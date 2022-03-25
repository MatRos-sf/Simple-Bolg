from django import forms

from .models import Comment


class CommentForms(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body',)

class ShareForm(forms.Form):
    name = forms.CharField(max_length=50)
    to = forms.EmailField()
    message = forms.CharField(required=False,
                              widget=forms.Textarea)