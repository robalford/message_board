from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post', ]
        widgets = {'post': forms.TextInput}


class LoatheForm(forms.Form):
    post_id = forms.CharField(widget=forms.HiddenInput)


