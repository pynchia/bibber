from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$',
            views.PlayGameView.as_view(),
            name='playgame'),
        url(r'^setup/$',
            views.SetUpGameView.as_view(),
            name='setupgame'),
]

