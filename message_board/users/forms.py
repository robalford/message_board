from django.forms import modelformset_factory

from message_board.posts.models import Peeve

PeeveFormSet = modelformset_factory(Peeve, fields=('peeve', ))
