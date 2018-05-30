from django import forms

from .models import BlockAccount

class InitiateTransactionForm(forms.Form):
    sender_address = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Sender address'}))
    sender_private_key = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Sender private key'}))
    recipient_address = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Recipient address'}))
    amount_to_send = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'step': 0.25, 'placeholder' : 'Amount to send: steps of 0.25'}))

class InitiateTransactionAuthUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(InitiateTransactionAuthUserForm, self).__init__(*args, **kwargs)
        self.fields['sender'].queryset = BlockAccount.objects.filter(owner__user=user)
        self.fields['recipient'].queryset = BlockAccount.objects.exclude(owner__user=user)

    sender = forms.ModelChoiceField(
        queryset=BlockAccount.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class' : 'form-control'}))
    recipient = forms.ModelChoiceField(
        queryset=BlockAccount.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class' : 'form-control'}))
    amount_to_send = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'step': 0.25}))

class AcceptTransactionForm(forms.Form):
    sender_address = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    recipient_address = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    signature = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    amount_to_receive = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'step': 0.25}))

class NodeRegistrationForm(forms.Form):
    node_urls = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Comma-separated list e.g http://127.0.0.1:5000'}))

class EditAliasForm(forms.ModelForm):
    class Meta:
        model = BlockAccount
        fields = ('alias', )

        widgets = {'alias' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Account identifier'})}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(EditAliasForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = BlockAccount.objects.filter(owner__user=user)

    account = forms.ModelChoiceField(
        queryset=BlockAccount.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class' : 'form-control'}))
