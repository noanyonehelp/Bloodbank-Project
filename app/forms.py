from django import forms
from .models import Comment, BloodBank

class BloodBankCreationForm(forms.ModelForm):
    bloodbank_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'اﻻسم', 'autofocus': 'autofocus'}), help_text='اﻻسم')

    bloodbank_addr = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'العنوان '}), help_text='العنوان')

    mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'رقم الهاتف المحمول: Mobile Number'}), help_text='رقم الهاتف المحمول', max_length=11, initial='01')

    class Meta:
        model = BloodBank
        fields = '__all__'

class CommentForm(forms.ModelForm):
    userProfile = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'disabled':'true'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'اكتب التعليق هنا', 'cols':2, 'rows':3}))
    class Meta:
        model = Comment
        fields = ['userProfile', 'comment']