from django.core.urlresolvers import reverse_lazy
from django.views import generic

from .prj_constants import *


class HomePage(generic.RedirectView):
    permanent = False
    url = reverse_lazy('play:setupgame')

