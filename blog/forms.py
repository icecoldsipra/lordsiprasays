from django import forms
from .models import Category, Comment, ContactMe, Post


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['tag']


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Category.objects.all(),
        required=False
    )

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
        model = ContactMe
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Type your name here...'}),
            'email': forms.TextInput(attrs={'type': 'email', 'placeholder': 'Type your email here...'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Type the subject here...'}),
            'message': forms.Textarea(attrs={'placeholder': 'Type the message here...'}),
        }
