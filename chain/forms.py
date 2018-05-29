from urllib.parse import urlparse

from django import forms

class InitiateTransactionForm(forms.Form):
    sender_address = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    sender_private_key = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    recipient_address = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    amount_to_send = forms.DecimalField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'step': 0.25}))

class AcceptTransactionForm(forms.Form):
    sender_address = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    recipient_address = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    signature = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    amount_to_receive = forms.DecimalField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'step': 0.25}))

class NodeRegistrationForm(forms.Form):
    node_urls = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Comma-separated list e.g http://127.0.0.1:5000'}))
