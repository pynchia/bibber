from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
#from django.conf import settings
from bibber.prj_constants import *
import random
import itertools as it
from .forms import GameSetUpForm


class Player(object):
    def __init__(self, name):
        self.pos = 0  # on which card I am
        self.free = True  # am I in prison
        self.name = name  # which player I am


class Card(object):
    def __init__(self, pos):
        self.pos = pos
        self.occupants = []
        self.covered = True
        self.captured = False

    def filename(self):
        if self.covered:
            name = 'covered.png'
        else:
            name = '%s%s%s.png' % (self.face,
                                   ''.join(self.occupants),
                                   'c' if self.captured else '') 
        return name

    def __unicode__(self):
        return 'face=%s captured=%s occupants=%s' % (self.face,
                                                     self.captured,
                                                     self.occupants)

    def __str__(self):
        return self.__unicode__()


def is_dest_allowed(pos, delta, players):
    xp = pos % CARDS_PER_ROW
    yp = pos / CARDS_PER_ROW
    dest = pos + delta
    if dest < 0 or dest >= NUM_CARDS:
        # out of board
        return False
    if dest in DISALLOWED_DESTINATIONS:
        # further investigation is required
        prisoners = [p.pos for p in players if not p.free]
        if dest not in prisoners:
            # no other player to be freed at that destination
            return False

    xd = dest % CARDS_PER_ROW
    yd = dest / CARDS_PER_ROW
    return any((xp == xd, yp == yd))


def find_destinations(pos, hops, players):
    """return the possible cards where I can land
    starting from card pos in hops hops"""
    dests = set()
    deltas = (-1, 1, -CARDS_PER_ROW, CARDS_PER_ROW)
    possibs4one_hop = [pos+d for d in deltas if is_dest_allowed(pos,
                                                                d, players)]
    if hops:
        for p in possibs4one_hop:
            dests.update(find_destinations(p, hops-1, players))
        return dests
    else:
        return possibs4one_hop


def setup_board(num_players):
    cards = [Card(i) for i in xrange(NUM_CARDS)]
    indexes = range(NUM_CARDS)
    prison3 = indexes.pop(CARDS_PER_ROW * 4 - 1)
    prison2 = indexes.pop(CARDS_PER_ROW * 3)
    prison1 = indexes.pop(CARDS_PER_ROW - 1)
    entrance = indexes.pop(0)
    random.shuffle(indexes)
    key1 = indexes.pop()
    key2 = indexes.pop()
    for _, ghost_type in zip(xrange(NUM_GHOST_CARDS),
                             it.cycle(CARD_GHOST_TYPES)):
        cards[indexes.pop()].face = ghost_type

    cards[entrance].face = CARD_ENTRANCE
    cards[entrance].covered = False
    cards[entrance].occupants = [str(p) for p in xrange(num_players)]
    cards[prison1].face = CARD_PRISON_CELL
    cards[prison1].covered = False
    cards[prison2].face = CARD_PRISON_CELL
    cards[prison2].covered = False
    cards[prison3].face = CARD_PRISON_CELL
    cards[prison3].covered = False
    cards[key1].face = CARD_PRISON_KEY
    cards[key2].face = CARD_PRISON_KEY

    #for i, card in enumerate(cards):
    #    print i, card
    return cards


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
        self.request.session[KEY_NUM_PLAYERS] = num_players
        self.request.session[KEY_PLAYERS] = [Player(str(name)) for name
                                             in xrange(num_players)]
        self.request.session[KEY_CUR_PLAYER] = num_players-1
        self.request.session[KEY_CLOCK] = 0
        self.request.session[KEY_BOARD] = setup_board(num_players)
        self.request.session[KEY_GAME_IS_ON] = True
        return super(SetUpGameView, self).form_valid(form)


class PlayView(GameMustBeOnMixin, generic.TemplateView):
    template_name = 'play/play.html'

    def get(self, request, *args, **kwargs):
        # advance to the next player
        cur_player = self.request.session[KEY_CUR_PLAYER]
        print 'cur_player', cur_player
        players = self.request.session[KEY_PLAYERS]
        player = players[cur_player]
        #free_players = [p for p in players if p.free]
        #if len(free_players) == 1:
        #    next_player = int(free_players[0].name)
        #else:
        cy_players = it.cycle(players)
        while next(cy_players) != player:
            pass
        while True:
            next_player = next(cy_players)
            if next_player.free:
                break
        print 'next_player', next_player.name

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
        else:
            # time must advance
            clock = self.request.session[KEY_CLOCK] + 1
            self.request.session[KEY_CLOCK] = clock
            if clock > 11:  # time is up, game over
                self.request.session[KEY_GAME_IS_ON] = False

        return super(MoveView, self).get(request, *args, **kwargs)


class ShowMoveView(GameMustBeOnMixin, generic.TemplateView):
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
            # make dest the first avail prison cell
            free_prisons = (c for c in cards
                            if c.face == CARD_PRISON_CELL and
                            not c.occupants)
            dest_card = next(free_prisons)
            # move the player in the prison
            player.pos = dest_card.pos
            player.free = False
            free_players = [p for p in players if p.free]
            if len(free_players) == 0:
                # all the players are in prison, GAME OVER!
                self.request.session[KEY_GAME_IS_ON] = False
        elif dest_card.face == CARD_PRISON_CELL:
            # it's a prison and it's a rescue op
            prisoner = next((p for p in players
                             if p.name in dest_card.occupants))
            prisoner.free = True
        elif not dest_card.captured:  # it's a free ghost
            ghosts_where_players = [cards[p.pos].face for p in players
                                    if not cards[p.pos].captured]
            if len(ghosts_where_players) == len(players) and \
               len(set(ghosts_where_players)) == 1:
                # all the players are on the same type of free ghost
                for p in players:
                    cards[p.pos].captured = True

        # finish placing the player on the dest card
        dest_card.occupants.append(player.name)
        dest_card.occupants.sort()
        # update the session
        self.request.session[KEY_BOARD] = cards
        self.request.session[KEY_PLAYERS] = players

        return super(ShowMoveView, self).get(request)

