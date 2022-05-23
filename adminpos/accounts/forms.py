from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django import forms
from django.db.models import Q
from django.contrib.auth.forms import SetPasswordForm


class UserRegisterForm(UserCreationForm):

    class Meta:
        model=get_user_model()
        fields=('username','password1','password2','profile_pic')
        
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'UserName','id':'user_username'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password','id':'user_userpass'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password','id':'user_userpassreenter'}),
            'profile_pic':forms.FileInput(attrs={'id':'user_userimage'})
        }

    def clean_username(self):
        username=self.cleaned_data['username']
        if get_user_model().objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('User already exist with this username')
        return username 
    
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['profile_pic'].label='Image'
        self.fields['username'].label='UserName'
        self.fields['password1'].label='Password'
        self.fields['password2'].label='Re-enter Password'
        self.fields['password1'].help_text=None
        
    
    def save(self,commit=True):
        user=super(UserRegisterForm,self).save(commit=False)
        if 'profile_pic' in self.cleaned_data:
            user.profile_pic=self.cleaned_data['profile_pic']
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    username = UsernameField(
        label='',
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'})
    )
    password=forms.CharField(
        label="",
        strip=False ,
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),
    )

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model=get_user_model()
        fields=('username','profile_pic')
        
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'UserName','id':'user_username'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password','id':'user_userpass'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password','id':'user_userpassreenter'}),
            'profile_pic':forms.FileInput(attrs={'id':'user_userimage'})
        }

    def __init__(self,*args, **kwargs):
        self.active_user=kwargs.pop('current_user')
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].label='Image'
        self.fields['username'].label='UserName'

    def clean_username(self):
        username=self.cleaned_data['username']
        if get_user_model().objects.filter(~Q(username__iexact=self.active_user.username),Q(username__iexact=username)).exists():
            raise forms.ValidationError('User with this username already exists..')
        return username
    
    def save(self,commit=True):
        user=super(UserUpdateForm,self).save(commit=False)
        if 'profile_pic' in self.cleaned_data:
            user.profile_pic=self.cleaned_data['profile_pic']
        if commit:
            user.save()
        return user

class UserPasswordChangeForm(SetPasswordForm):

    def __init__(self,*args, **kwargs):
        pk=kwargs.pop('pk')
        self.change_user=get_user_model().objects.get(pk=pk)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.change_user.set_password(password)
        if commit:
            self.change_user.save()
        return self.change_user	


        
        




    
