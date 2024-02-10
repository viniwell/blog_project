from django import forms
from .models import Shop_Post, Size, Comment, Profile
from django.contrib.auth.models import User


class ShopPostForm(forms.ModelForm):
    class Meta:
        model=Shop_Post
        fields=['title', 'body',"size", "status"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
        # exclude=[...]

class RegisterForm(forms.ModelForm):
    password=forms.CharField(label='Enter password', widget=forms.PasswordInput())
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=["username", 'first_name', 'last_name', 'email']
    
    def clean_password2(self):
        if self.cleaned_data['password']!=self.cleaned_data['password2']:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data['password2']
    
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('This email is already in use')
        return self.cleaned_data['email']
    
class LoginForm(forms.Form):
    username=forms.CharField(empty_value='Enter your username or email', label='Enter your username or email')
    password=forms.CharField(widget=forms.PasswordInput(), empty_value='Enter password',)

