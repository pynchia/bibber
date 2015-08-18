from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
#from django.conf import settings
from bibber.prj_constants import *
from .forms import GameSetUpForm


class Card(object):
    def __init__(self, numcard):
        self.numcard = numcard

    def __unicode__(self):
        return self.numcard


class SetUpGameView(generic.FormView):
    form_class = GameSetUpForm
    initial = {'num_players': '3'}
    template_name = 'play/setup.html'
    success_url = reverse_lazy('play:playgame')

    def form_valid(self, form):
        # set the session vars
        self.request.session[KEY_NUM_PLAYERS] = \
                                    form.cleaned_data['num_players']
        self.request.session[KEY_GAME_IS_ON] = True
        cards = [Card(i) for i in range(24)]
        print 'cards', cards
        self.request.session[KEY_BOARD] = cards
        # print "Numplayers=", form.cleaned_data['num_players']
        return super(SetUpGameView, self).form_valid(form)


class PlayGameView(generic.TemplateView):
    template_name = 'play/play.html'

