from django import forms
from .models import Coment
from .models import Post


class EmilPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)
    
class ComentForm(forms.ModelForm):
    class Meta:
        model = Coment
        fields = ['name', 'email', 'body']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'status', 'author', 'tags']