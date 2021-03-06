import random
import itertools as it
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponseForbidden

from prj_constants import *
from common import *
from .forms import GameSetUpForm


class GameMustBeOnMixin(object):
    """mixin to allow playing only if the game is on"""
    def dispatch(self, request, *args, **kwargs):
        if request.session[KEY_GAME_IS_ON]:
            return super(GameMustBeOnMixin, self).dispatch(request,
                                                           *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('play:setupgame'))


class SetUpGameView(generic.FormView):
    form_class = GameSetUpForm
    initial = {'num_players': '3'}
    template_name = 'play/setup.html'
    success_url = reverse_lazy('play:playgame')

    def form_valid(self, form):
        # set the session vars
        num_players = int(form.cleaned_data['num_players'])
        setup_game(self.request, num_players)
        return super(SetUpGameView, self).form_valid(form)


class PlayView(GameMustBeOnMixin, generic.TemplateView):
    template_name = 'play/play.html'

    def get(self, request, *args, **kwargs):
        # advance to the next player
        cur_player = self.request.session[KEY_CUR_PLAYER]
        players = self.request.session[KEY_PLAYERS]
        player = players[cur_player]
        cy_players = it.cycle(players)
        while next(cy_players) != player:
            pass
        while True:
            next_player = next(cy_players)
            if next_player.free:
                break
        self.request.session[KEY_CUR_PLAYER] = int(next_player.name)
        # cover any key left flipped up
        cards = self.request.session[KEY_BOARD]
        for c in cards:
            if c.face == CARD_PRISON_KEY:
                c.covered = True
        self.request.session[KEY_BOARD] = cards

        return super(PlayView, self).get(request, *args, **kwargs)


class MoveView(GameMustBeOnMixin, generic.TemplateView):
    template_name = 'play/move.html'

    def get(self, request, *args, **kwargs):
        self.die = random.choice(DIE_VALUES)
        if self.die > 0:
            cur_player = self.request.session[KEY_CUR_PLAYER]
            players = self.request.session[KEY_PLAYERS]
            player = players[cur_player]
            self.possib_dest = find_destinations(player.pos,
                                                 self.die-1,
                                                 players)
            self.request.session[KEY_POSSIB_DEST] = self.possib_dest
        else:
            # time must advance
            clock = self.request.session[KEY_CLOCK] + 1
            self.request.session[KEY_CLOCK] = clock
            if clock > 11:  # time is up, game over
                self.request.session[KEY_GAME_IS_ON] = False
                self.sound = SOUND_CLOCK12
            else:
                self.sound = SOUND_CLOCK

        return super(MoveView, self).get(request, *args, **kwargs)


class ShowMoveView(GameMustBeOnMixin, generic.TemplateView):
    template_name = 'play/show.html'

    def get(self, request, dest):
        dest = int(dest)
        if dest not in self.request.session[KEY_POSSIB_DEST]:
            return HttpResponseForbidden('<h1>Invalid destination</h1>')

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
            self.sound = SOUND_PATH+'ghost%d.mp3' % \
                                          random.randint(0, SOUND_MAX_GHOSTS)
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

