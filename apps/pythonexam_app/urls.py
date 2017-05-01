from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.home),
    url(r'^main$', views.index),
    url(r'^reg$', views.reg),
    url(r'^login$', views.login),
    url(r'^quotes$', views.quotes),
    url(r'^logout$', views.logout),
    url(r'^addquote$', views.addquote),
    url(r'^addfav/(?P<Quote_id>\d+)$', views.addfav),
    url(r'^removefav/(?P<Quote_id>\d+)$', views.removefav),
    url(r'^user/(?P<User_id>\d+)$', views.userpage),  
]
