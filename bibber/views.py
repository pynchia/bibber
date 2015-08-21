from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic

from .prj_constants import *


class HomePage(generic.RedirectView):
    permanent = False

    def get_redirect_url(self):
        """redirect to the appropriate page based on the status of the game
        which reflects its progress
        """
        dest = {STATUS_OFF: 'play:setupgame',
                STATUS_START: 'play:playgame',
               }[self.request.session.get(KEY_GAME_STATUS, STATUS_OFF)]
        return reverse(dest)

