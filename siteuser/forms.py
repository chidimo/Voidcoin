"""Forms"""

from django import forms
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import SiteUser, Wallet

CustomUser = get_user_model()

class UserCreationForm(forms.ModelForm):
    """Custom UCF. Takes the standard
    variables of 'email', 'password1', 'password2'
    For creating instances of 'CustomUser'."""
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))

    class Meta:
        model = CustomUser
        fields = ('email', )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = CustomUser
        fields = ["email", "password", "is_active", "is_admin"]

    def clean_password(self):
        return self.initial["password"]

class SiteUserMixin(forms.ModelForm):
    class Meta:
        model = SiteUser
        fields = ("screen_name", )
        widgets = {
            "screen_name" : forms.TextInput(attrs={'class':'form-control', "placeholder" : "Display name"}),
        }

class SiteUserRegistrationForm(forms.Form):
    screen_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control', "placeholder" : "Screen name"}))

    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control', "placeholder" : "Email address"}))

    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', "placeholder" : "Enter password"}))

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', "placeholder" : "Verify password"}))

    def clean(self):
        data = self.cleaned_data
        email = data.get("email", None).strip()
        password1 = data.get('password1', None).strip()
        password2 = data.get('password2', None).strip()
        screen_name = data.get("screen_name", None).strip()

        User = get_user_model()
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Email already registered.')

        if password1 and password2 and password1 != password2:
            self.add_error('password1', "Passwords do not match")

        if SiteUser.objects.filter(screen_name=screen_name).exists():
            self.add_error('screen_name', 'Display name already taken.')

class SiteUserEditForm(forms.ModelForm):
    class Meta:
        model = SiteUser
        fields = ["screen_name",]

        widgets = {
            "screen_name" : forms.TextInput(attrs={'class' : 'form-control', "placeholder" : "Screen name"}),
        }

class PassWordGetterForm(forms.Form):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', "placeholder" : "Enter password"}))
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PassWordGetterForm, self).__init__(*args, **kwargs)

    def clean(self):
        password = self.cleaned_data['password']
        if check_password(password, self.user.password) is False:
            self.add_error('password', 'You entered a wrong password')

class EditAliasForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ('alias', )

        widgets = {'alias' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Account identifier'})}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(EditAliasForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Wallet.objects.filter(owner__user=self.user)

    account = forms.ModelChoiceField(
        queryset=Wallet.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class' : 'form-control'}))

    def clean(self):
        alias = self.cleaned_data['alias']
        aliases = Wallet.objects.filter(owner__user=self.user).values_list('alias', flat=True)
        if alias in aliases:
            self.add_error('alias', "You already have a wallet name {}".format(alias))
