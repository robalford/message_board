from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.message_board_view, name='message_board'),
    url(r'^commiserate/(?P<post_id>\d+)/$', views.commiserate_view, name='commiserate'),
]
