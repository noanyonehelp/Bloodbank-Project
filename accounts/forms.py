from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'autofocus':'true', 'class':'fname'}), label='اﻻسم الأول', help_text='اﻻسم الأول لا يمكن أن يكون فارغًا')

    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'autofocus':'true', 'class':'lname'}), label='اﻻسم الأخير', help_text='اﻻسم الأخير لا يمكن أن يكون فارغًا')

    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput, label='اسم المستخدم', help_text='من الأفضل أن يحتوي على حروف وأرقام، وألا يكون مستخدمًا من قبل')

    email = forms.CharField(max_length=100, required=True, widget=forms.EmailInput, label='البريد الالكتروني', help_text='أدخل البريد بصورة صحيحة حتى يمكن استعادة كلمة السر أثناء نسيانها عن طريقه')

    password1 = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput, label='كلمة السر', help_text='اختر كلمة سر مكونة من حروف كبيرة وصغيرة وأرقام ورموز')

    password2 = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput, label='تأكيد كلمة السر', help_text='تأكد من تطابق كلمة السر في الحقلين لتجنب الخطأ أثناء التسجيل')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']