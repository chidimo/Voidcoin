from django import forms
from siteuser.models import Wallet

class AcceptTransactionForm(forms.Form):
    sender_address = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    recipient_address = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    signature = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    amount_to_receive = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'step': 0.25}))

class NodeRegistrationForm(forms.Form):
    node_urls = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Comma-separated list e.g http://127.0.0.1:5000'}))

class InitiateTransactionForm(forms.Form):
    sender_address = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Sender address'}))
    sender_private_key = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Sender private key'}))
    recipient_address = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Recipient address'}))
    amount_to_send = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'step': 0.25, 'placeholder' : 'Amount to send: steps of 0.25'}))

class InitiateTransactionAuthUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(InitiateTransactionAuthUserForm, self).__init__(*args, **kwargs)
        self.fields['wallet'].queryset = Wallet.objects.filter(owner__user=user)

    def clean(self):
        data = self.cleaned_data
        wallet = data['wallet']
        recipient = data['recipient']
        amount_to_send = data['amount_to_send']
        if wallet == recipient:
            self.add_error('recipient', 'Wallet cannot transfer to itself')
        if wallet.balance < amount_to_send:
            self.add_error('wallet', 'Low wallet balance: {}'.format(wallet.balance))

    wallet = forms.ModelChoiceField(
        queryset=Wallet.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class' : 'form-control'}))
    recipient = forms.ModelChoiceField(
        queryset=Wallet.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class' : 'form-control'}))
    amount_to_send = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'step': 0.25}))
