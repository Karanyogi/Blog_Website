from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfileInfo, Post




class UserProfileInfoForm(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = ('first_name','last_name','phone')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['phone'].label = "Mobile Number"


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('username','email','password1','password2')
        model = get_user_model()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = "Username"
        self.fields['email'].label = "Email Address"
        self.fields['password1'].label = "Set a Password"
        self.fields['password2'].label = "confirm password"





class PostForm(forms.ModelForm):
    class Meta():
        fields=("heading","message")
        # widgets = {'manager': forms.HiddenInput()}
        model=Post

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["heading"].label = "Heading"
        self.fields["message"].label = "Write Blog"
