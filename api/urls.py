#from django.conf.urls import url, include
#from rest_framework.routers import DefaultRouter
from . import views

# in case you want a browsable API (sort of)
#router = DefaultRouter()
#router.register('setup', views.SetUpGameView, base_name='setup')
#router.register('next', views.NextTurnView, base_name='next')
#router.register('draw', views.DrawDieView, base_name='draw')
#router.register('pick', views.PickDestView, base_name='pick')

urlpatterns = [
#    url(r'^',
#        include(router.urls)),
        url(r'^setup/$',
            views.SetUpGameView.as_view(),
            name='setupgame'),
        url(r'^next/$',
            views.NextTurnView.as_view(),
            name='next'),
        url(r'^draw/$',
            views.DrawDieView.as_view(),
            name='draw'),
        url(r'^pick/$',
            views.PickDestView.as_view(),
            name='pick'),
]
