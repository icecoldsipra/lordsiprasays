from django import forms
from .models import Comment, Contact, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'tags', 'image', 'is_live', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
        widgets = {
          'content': forms.Textarea(attrs={'rows': 3}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
