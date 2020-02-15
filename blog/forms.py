from django import forms
from .models import Comment, Contact, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'tags', 'image', 'is_live', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type the comment here...'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Type your name here...'}),
            'email': forms.TextInput(attrs={'type': 'email', 'placeholder': 'Type your email here...'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Type the subject here...'}),
            'message': forms.Textarea(attrs={'placeholder': 'Type the message here...'}),
        }
