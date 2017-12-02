from django.db import models

from message_board.users.models import User


class Peeve(models.Model):
    peeve = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='peeves')

    def __str__(self):
        return self.peeve


class Post(models.Model):
    post = models.TextField(blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    post_date = models.DateTimeField(auto_now_add=True)
    response_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='responses')
    loathes = models.ManyToManyField(User, blank=True, related_name='loathed_posts')
    peeves = models.ManyToManyField(Peeve, blank=True)

    class Meta:
        ordering = ['-post_date', ]

    def __str__(self):
        return '{} on {}'.format(self.posted_by, self.post_date.strftime("%B %d, %Y"))
