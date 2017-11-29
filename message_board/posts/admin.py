from django.contrib import admin

from message_board.posts.models import Peeve, Post

admin.site.register(Peeve)
admin.site.register(Post)
