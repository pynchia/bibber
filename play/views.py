from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
#from django.conf import settings
from bibber.prj_constants import *
import random
from itertools import izip, cycle
from .forms import GameSetUpForm


class Card(object):
    def __init__(self):
        self.num_occupants = 0

    def __unicode__(self):
        return 'num_occupants=%d face=%s' % (self.num_occupants, self.face)

    def __str__(self):
        return self.__unicode__()


def setup_board():
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
        self.request.session[KEY_NUM_PLAYERS] = \
                                    form.cleaned_data['num_players']
        # print "Numplayers=", form.cleaned_data['num_players']
        self.request.session[KEY_GAME_STATUS] = STATUS_PLAY

        self.request.session[KEY_BOARD] = setup_board()
        return super(SetUpGameView, self).form_valid(form)


class PlayGameView(generic.TemplateView):
    template_name = 'play/play.html'

