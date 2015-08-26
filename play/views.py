from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
#from django.conf import settings
from bibber.prj_constants import *
import random
from itertools import izip, cycle
from .forms import GameSetUpForm


class Card(object):
    def __init__(self):
        self.occupants = []
        self.captured = False

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
    for _, ghost_type in izip(
                          xrange(NUM_GHOST_CARDS), cycle(CARD_GHOST_TYPES)):
        cards[indexes.pop()].face = ghost_type
    cards[entrance].face = CARD_ENTRANCE
    cards[entrance].occupants = ['p%d' % (i,) for i in xrange(1,
                                                              num_players+1)]
    cards[prison1].face = CARD_PRISON_CELL
    cards[prison2].face = CARD_PRISON_CELL
    cards[prison3].face = CARD_PRISON_CELL
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
        # print "Numplayers=", form.cleaned_data['num_players']
        self.request.session[KEY_GAME_STATUS] = STATUS_PLAY

        self.request.session[KEY_BOARD] = setup_board(num_players)
        return super(SetUpGameView, self).form_valid(form)


class PlayGameView(generic.TemplateView):
    template_name = 'play/play.html'

