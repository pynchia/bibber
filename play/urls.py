from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^play/$',
            views.PlayView.as_view(),
            name='playgame'),
        url(r'^move/$',
            views.MoveView.as_view(),
            name='move'),
        url(r'^show/(?P<dest>\d+)/$',
            views.ShowMoveView.as_view(),
            name='showmove'),
        url(r'^setup/$',
            views.SetUpGameView.as_view(),
            name='setupgame'),
]

