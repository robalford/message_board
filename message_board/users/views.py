from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect, render

from message_board.posts.models import Peeve
from .forms import PeeveFormSet
from .models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', 'profile_pic', ]

    # we already imported User in the view code above, remember?
    model = User

    template_name = 'users/user_form.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        formset = PeeveFormSet(queryset=Peeve.objects.filter(users=self.request.user))
        context['formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        formset = PeeveFormSet(request.POST, queryset=Peeve.objects.filter(users=self.request.user))
        if formset.is_valid():
            for f in formset:
                if f.instance.peeve:
                    peeve, created = Peeve.objects.get_or_create(peeve=f.instance.peeve)
                    peeve.users.add(self.request.user)
                    peeve.save()
            super().post(request, *args, **kwargs)
            return redirect(reverse('users:detail', kwargs={'username': self.request.user.username}))
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
