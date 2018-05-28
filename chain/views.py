import json

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_POST

import binascii
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

from .blockchain_client import Transaction
from .forms import TransactionGeneratorForm

def transactions_index(request):
    template = 'chain/transactions_index.html'
    context = {}
    return render(request, template, context)

def make_transaction(request):
    template = 'chain/make_transaction.html'
    context = {}
    messages.success(request, "Transaction completed successfully")
    return redirect(reverse('blockchain:view_transaction'))

def view_transaction(request):
    template = 'chain/view_transaction.html'
    context = {}
    return render(request, template, context)

def generate_wallet(request):
    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(1024, random_gen)
    public_key = private_key.publickey()
    context = {
        'private_key' : binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
        'public_key' : binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
        }
    # return redirect(reverse('blockchain:index'))
    messages.success(request, "New wallet generated successfully")
    return HttpResponse(json.dumps(context), content_type='application/json')

# @require_POST
def generate_transaction(request):
    template = 'chain/generate_transaction.html'
    context = {}

    if request.method == 'POST':
        form = TransactionGeneratorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            sender_address = data['sender_address']
            sender_private_key = data['sender_private_key']
            recipient_address = data['recipient_address']
            amount_to_send = data['amount_to_send']

            transaction = Transaction(sender_address, sender_private_key, recipient_address, amount_to_send)
            context['transaction'] = transaction.to_dict()
            context['signature'] = transaction.sign_transaction()
            messages.success(request, "Transaction generated successfully")
            # return redirect(reverse('blockchain:index'))
            return HttpResponse(json.dumps(context), content_type='application/json')
        else:
            return render(request, template, {'form' : form})
    return render(request, template, {'form' : TransactionGeneratorForm()})

def index(request):
    template = 'chain/index.html'
    context = {}
    context['blockchain'] = settings.BLOCKCHAIN
    return render(request, template, context)
