from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic

from .prj_constants import *


class HomePage(generic.RedirectView):
    permanent = False

    def get_redirect_url(self):
        # if game is off
        if self.request.session.get(KEY_GAME_IS_ON, None):
            print "Game is On"
            return reverse('play:playgame')
        else:
            print "Game is Off"
            return reverse('play:setupgame')

