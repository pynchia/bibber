from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
#from django.conf import settings
from bibber.prj_constants import *
import random
import itertools as it
from .forms import GameSetUpForm


class Player(object):
    def __init__(self, num):
        self.num = num
        self.pos = 0
        self.free = True


class Card(object):
    def __init__(self):
        self.occupants = []
        self.covered = False
        self.captured = False
        self.possib_dest = False

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


def setup_board(num_players):
    cards = [Card() for _ in xrange(NUM_CARDS)]
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
        self.request.session[KEY_DIE] = 0
        self.request.session[KEY_GAME_STATUS] = STATUS_PLAY

        self.request.session[KEY_BOARD] = setup_board(num_players)
        return super(SetUpGameView, self).form_valid(form)


class PlayView(generic.TemplateView):
    template_name = 'play/play.html'


class MoveView(generic.TemplateView):
    template_name = 'play/move.html'

    def get(self, request, *args, **kwargs):
        draw = random.choice(DIE_VALUES)
        request.session[KEY_DIE] = draw
        if not draw:  # the clock!
            # time must advance...
            pass

        return super(MoveView, self).get(request, *args, **kwargs)

