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
        self.name = name  # which player I am
        self.pos = 0  # on which card I am
        self.free = True  # am I in prison


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


def is_dest_allowed(pos, delta):
    xp = pos % CARDS_PER_ROW
    yp = pos / CARDS_PER_ROW
    dest = pos + delta
    if dest < 0 or dest >= NUM_CARDS or dest in DISALLOWED_DESTINATIONS:
        return False
    xd = dest % CARDS_PER_ROW
    yd = dest / CARDS_PER_ROW
    return any((xp == xd, yp == yd))


def find_destinations(pos, hops):
    """return the possible cards where I can land
    starting from card pos in hops hops"""
    dests = set()
    deltas = (-1, 1, -CARDS_PER_ROW, CARDS_PER_ROW)
    possibs4one_hop = [pos+d for d in deltas if is_dest_allowed(pos, d)]
    if hops:
        for p in possibs4one_hop:
            dests.update(find_destinations(p, hops-1))
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
        players = self.request.session[KEY_PLAYERS]
        player = players[cur_player]
        free_players = [p for p in players if p.free]
        if len(free_players) == 1:
            next_player = int(free_players[0].name)
        else:
            cy_free_players = it.cycle(free_players)
            while next(cy_free_players) != player:
                pass
            next_player = int(next(cy_free_players).name)
        self.request.session[KEY_CUR_PLAYER] = next_player
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
            self.possib_dest = find_destinations(player.pos, self.die-1)
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
        if dest_card.face == CARD_PRISON_KEY:
            # the player must go to prison!
            # check if he's the last one free, if so GAME OVER
            free_players = [p for p in players if p.free]
            if len(free_players) == 1:
                self.request.session[KEY_GAME_IS_ON] = False
            else:
                # make dest the first avail prison cell
                free_prisons = (c for c in cards
                                if c.face == CARD_PRISON_CELL and
                                not c.occupants)
                dest_card = next(free_prisons)
                player.free = False

        # place the player on the dest card
        player.pos = dest_card.pos
        dest_card.occupants.append(player.name)
        dest_card.occupants.sort()
        # update the session
        self.request.session[KEY_BOARD] = cards
        self.request.session[KEY_PLAYERS] = players

        return super(ShowMoveView, self).get(request)

