from django import forms
from .models import Profile,Fef,Reply
from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
class UserRegistrationForm(forms.ModelForm):
    password=forms.CharField(label='password',widget=forms.PasswordInput)
    password2=forms.CharField(label='repeat password',widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','first_name','email']    
        def clean_password2(self):
            cd=self.cleaned_data
            if cd['password']!=cd['password2']:
                raise
            forms.ValidationError('passwords don\'t match')
            return cd['password2']
        #same here preventing users using same email
        def clean_mail(self):
            data=self.cleaned_data('email')
            if User.objects.filter(email=data).exists():
                raise
            forms.ValidationError('Email already in use.')
            return data
class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
        #preventing users from using existing email
        def clean_email(self):
            data=self.cleaned_data['email']
            qs=User.objects.exclude(id=self.instance.id).filter(email=data)
            if qs.exists():
                raise
            forms.ValidationError('email already in use')
            return data

class FefForm(forms.ModelForm):
    class Meta:
        model=Fef
        exclude=('user','likes',)
        fields=['text','im','video','audio']
        labels={'text':'compose'}
        widgets={'text':forms.Textarea(attrs={'cols':80})}
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['photo']  
class ReplyForm(forms.ModelForm):
    class Meta:
        model=Reply
        exclude=('user',)
        fields=['body','repimg','repvideo','audio2']
        labels={'body':''}        
            