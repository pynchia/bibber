from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
#from django.conf import settings as st
from bibber.prj_constants import *
from .forms import GameSetUpForm


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
        # print "Numplayers=", form.cleaned_data['num_players']
        return super(SetUpGameView, self).form_valid(form)


class PlayGameView(generic.TemplateView):
    pass

