from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$',
            views.PlayView.as_view(),
            name='playgame'),
        url(r'^move/$',
            views.MoveView.as_view(),
            name='move'),
        url(r'^setup/$',
            views.SetUpGameView.as_view(),
            name='setupgame'),
]

