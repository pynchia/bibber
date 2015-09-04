import random
#from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from prj_constants import *
from common import *
from .serializers import *


class GameMustBeOnMixin(object):
    """mixin to allow playing only if the game is on"""
    def dispatch(self, request, *args, **kwargs):
        if request.session[KEY_GAME_IS_ON]:
            return super(GameMustBeOnMixin, self).dispatch(request,
                                                           *args, **kwargs)
        else:
            return Response(status.HTTP_403_FORBIDDEN)


class SetUpGameView(APIView):
    """setup the game
    Input:  none
    Output: 'num_players': int
    """
    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            num_players = serializer.validated_data['num_players']
            setup_game(request, num_players)
            return Response({KEY_NUM_PLAYERS: num_players},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NextTurnView(GameMustBeOnMixin, APIView):
    """advance the turn to the next player.
    Input:  none
    Output: 'clock': int
            'board': list of cards
                        [
                         { "captured": bool,
                           "covered": bool,
                           "filename": "/static/cell.png",
                           "occupants": [ in1, int2, ...],
                           "pos": int
                         }
                        ]

            'cur_player': int
    """
    def get(self, request):
        cur_player = advance_to_next_player(request)
        # cover any key left flipped up
        cards = request.session[KEY_BOARD]
        for c in cards:
            if c.face == CARD_PRISON_KEY:
                c.covered = True
        request.session[KEY_BOARD] = cards
        se_cards = CardSerializer(cards, many=True)
        return Response({KEY_CLOCK: request.session[KEY_CLOCK],
                         KEY_BOARD: se_cards.data,
                         KEY_CUR_PLAYER: cur_player},
                        status=status.HTTP_200_OK)


class DrawDieView(GameMustBeOnMixin, APIView):
    def get(self, request):
        ret_params = {}
        die = random.choice(DIE_VALUES)
        ret_params[KEY_DIE] = die
        if die > 0:
            cur_player = request.session[KEY_CUR_PLAYER]
            players = request.session[KEY_PLAYERS]
            player = players[cur_player]
            possib_dest = find_destinations(player.pos,
                                            die-1,
                                            players)
            ret_params[KEY_POSSIB_DEST] = possib_dest
            ret_params[KEY_GAME_IS_ON] = True
        else:
            # time must advance
            clock = request.session[KEY_CLOCK] + 1
            request.session[KEY_CLOCK] = clock
            if clock > 11:  # time is up, game over
                request.session[KEY_GAME_IS_ON] = False
                ret_params[KEY_GAME_IS_ON] = False
            else:
                ret_params[KEY_CLOCK] = clock
                ret_params[KEY_GAME_IS_ON] = True

        return Response(ret_params,
                        status=status.HTTP_200_OK)


class PickDestView(GameMustBeOnMixin, APIView):
    template_name = 'play/show.html'

    def get(self, request, dest):
        dest = int(dest)
        cur_player = self.request.session[KEY_CUR_PLAYER]
        players = self.request.session[KEY_PLAYERS]
        player = players[cur_player]
        cards = self.request.session[KEY_BOARD]
        source_card = cards[player.pos]
        # remove the player from the source card
        source_card.occupants.remove(player.name)
        if not source_card.captured and len(source_card.occupants) == 0 \
           and player.pos not in DISALLOWED_DESTINATIONS:
            # cover the source card again
            source_card.covered = True
        dest_card = cards[dest]
        # flip the destination card
        dest_card.covered = False
        # partially put the player on the card
        player.pos = dest_card.pos
        if dest_card.face == CARD_PRISON_KEY:
            # the player must go to prison!
            # find the first avail prison cell
            free_prisons = [c for c in cards
                            if c.face == CARD_PRISON_CELL and
                            not c.occupants]
            dest_card = random.choice(free_prisons)
            # move the player in the prison
            player.pos = dest_card.pos
            player.free = False
            self.sound = SOUND_PRISON_KEY
            free_players = [p for p in players if p.free]
            if len(free_players) == 0:
                # all the players are in prison, GAME OVER!
                self.request.session[KEY_GAME_IS_ON] = False
                self.win = False
                self.sound = SOUND_GAME_OVER
        elif dest_card.face == CARD_PRISON_CELL:
            # it's a prison therefore it's a rescue op
            prisoner = next((p for p in players
                             if p.name in dest_card.occupants))
            prisoner.free = True
            self.sound = SOUND_PRISON_FREE
        elif not dest_card.captured:  # it's a free ghost
            ghosts_where_players = [cards[p.pos].face for p in players
                                    if not cards[p.pos].captured]
            self.sound = 'ghost%d' % random.randint(0, SOUND_MAX_GHOSTS)
            if len(ghosts_where_players) == len(players) and \
               len(set(ghosts_where_players)) == 1:
                # all the players are on the same type of free ghost
                for p in players:
                    cards[p.pos].captured = True
                    self.sound = SOUND_CAPTURED

            free_ghosts = [c for c in cards if c.face.startswith('ghost') and
                           not c.captured]
            if len(free_ghosts) == 0:
                # no more free ghosts, win the game!!!!
                self.request.session[KEY_GAME_IS_ON] = False
                self.win = True
                self.sound = SOUND_WIN

        # finish placing the player on the dest card
        dest_card.occupants.append(player.name)
        dest_card.occupants.sort()
        # update the session
        self.request.session[KEY_BOARD] = cards
        self.request.session[KEY_PLAYERS] = players

        return super(ShowMoveView, self).get(request)

