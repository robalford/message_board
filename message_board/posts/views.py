from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import PostForm
from .models import Post, Peeve


@login_required
def message_board_view(request, peeve=None):
    if peeve:
        peeve = get_object_or_404(Peeve, peeve=peeve)
        posts = get_list_or_404(Post, response_to=None, peeves=peeve)
    else:
        posts = Post.objects.filter(response_to=None)
    if request.method == 'POST':
        new_message_form = PostForm(request.POST)
        if new_message_form.is_valid():
            new_message = new_message_form.save(commit=False)
            new_message.posted_by = request.user
            new_message.save()
            # parse the post string to extract and save the tags (words prepended by an '!')
            post_as_list = new_message.post.split()
            for word in post_as_list:
                if word.startswith('!'):
                    word = word.lower()
                    peeve, _ = Peeve.objects.get_or_create(peeve=word)
                    new_message.peeves.add(peeve)
                    peeve.users.add(request.user)
                    peeve.save()
                    new_message.post = new_message.post.replace(word, '')
                    new_message.save()
            return redirect(reverse('message_board'))
    new_message_form = PostForm()
    commiserate_form = PostForm(prefix='commiserate')
    context = {
        'posts': posts,
        'new_message_form': new_message_form,
        'commiserate_form': commiserate_form,
    }
    return render(request, template_name='posts/message_board.html', context=context)


@require_POST
@login_required
def commiserate_view(request, post_id):
    commiserate_form = PostForm(request.POST, prefix='commiserate')
    if commiserate_form.is_valid():
        response = commiserate_form.save(commit=False)
        response.posted_by = request.user
        response.response_to = Post.objects.get(pk=post_id)
        response.save()
        return redirect(reverse('message_board'))
    else:
        messages.error(request, commiserate_form.errors)
        return redirect(reverse('message_board'))

