from django import forms

class TransactionGeneratorForm(forms.Form):
    sender_address = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    sender_private_key = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    recipient_address = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    amount_to_send = forms.DecimalField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'step': 0.25}))
