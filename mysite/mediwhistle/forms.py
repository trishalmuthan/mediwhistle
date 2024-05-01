from django import forms
from django.forms import ModelForm
from .models import Form


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}), label='Comment')

class YourForm(ModelForm):
    class Meta:
        model = Form
        fields = ['subject', 'name', 'email', 'doctor', 'location', 'practice', 'message', 'file']

        