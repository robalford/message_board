from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.message_board_view, name='message_board'),
    url(r'^peeves/(?P<peeve>[\w!-]+)$', views.message_board_view, name='peeves'),
    url(r'^commiserate/(?P<post_id>\d+)/$', views.commiserate_view, name='commiserate'),
    url(r'^loathe/$', views.loathe_view, name='loathe'),
]
