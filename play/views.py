from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
#from django.conf import settings
from bibber.prj_constants import *
import random
import itertools as it
from .forms import GameSetUpForm


class Player(object):
    def __init__(self, num):
        self.num = num  # which player I am
        self.pos = 0  # on which card I am
        self.free = True  # am I in prison


class Card(object):
    def __init__(self, pos):
        self.pos = pos
        self.occupants = []
        self.covered = False
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
    if dest < 0 or dest >= NUM_CARDS:
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


class SetUpGameView(generic.FormView):
    form_class = GameSetUpForm
    initial = {'num_players': '3'}
    template_name = 'play/setup.html'
    success_url = reverse_lazy('play:playgame')

    def form_valid(self, form):
        # set the session vars
        num_players = int(form.cleaned_data['num_players'])
        self.request.session[KEY_NUM_PLAYERS] = num_players
        players = [Player(num) for num in '123']
        self.request.session[KEY_PLAYERS] = players
        self.request.session[KEY_CUR_PLAYER] = 0
        self.request.session[KEY_CLOCK] = 0
        self.request.session[KEY_BOARD] = setup_board(num_players)
        return super(SetUpGameView, self).form_valid(form)


class PlayView(generic.TemplateView):
    template_name = 'play/play.html'


class MoveView(generic.TemplateView):
    template_name = 'play/move.html'

    def get_context_data(self, **kwargs):
        context = super(MoveView, self).get_context_data(**kwargs)
        draw = random.choice(DIE_VALUES)
        context['die'] = draw
        if draw > 0:
            cur_player = self.request.session[KEY_CUR_PLAYER]
            players = self.request.session[KEY_PLAYERS]
            player = players[cur_player]
            context['possib_dest'] = find_destinations(player.pos, draw-1)
        else:
            # time must advance...
            pass
        return context


