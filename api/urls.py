from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

#router = DefaultRouter()
#router.register('entries', views.EntryViewSet)

urlpatterns = [
#    url(r'^',
#        include(router.urls)),
#    url(r'^showurl/(?P<pk>\d+)/$',
#        views.ShowURLView.as_view(),
#        name='showurl'),
        url(r'^play/$',
            views.PlayView.as_view(),
            name='playgame'),
        url(r'^move/$',
            views.MoveView.as_view(),
            name='move'),
        url(r'^show/$',
            views.ShowMoveView.as_view(),
            name='showmove'),
        url(r'^setup/$',
            views.SetUpGameView.as_view(),
            name='setupgame'),
]
