import json

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_POST

import binascii
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

from .blockchain_client import Transaction, Blockchain
from .forms import InitiateTransactionForm, AcceptTransactionForm, NodeRegistrationForm

# Instantiate a blockchain
# BLOCKCHAIN = settings.BLOCKCHAIN
BLOCKCHAIN = Blockchain()
MINING_SENDER = ''
MINING_REWARD = ''
print("**********", BLOCKCHAIN)

def index(request):
    template = 'chain/index.html'
    context = {}
    context['blockchain'] = BLOCKCHAIN
    return render(request, template, context)

def transactions_index(request):
    template = 'chain/transactions_index.html'
    context = {}
    return render(request, template, context)

def make_transaction(request):
    # template = 'chain/make_transaction.html'
    # context = {}
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
def initiate_transaction(request):
    template = 'chain/initiate_transaction.html'
    context = {}

    if request.method == 'POST':
        form = InitiateTransactionForm(request.POST)
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
            return JsonResponse(context)
        else:
            return render(request, template, {'form' : form})
    return render(request, template, {'form' : InitiateTransactionForm()})

def validate_and_block_transaction(request):
    """Check if transaction is valid, accept it and add it to the block"""
    template = 'chain/validate_and_block_transaction.html'

    if request.method == 'POST':
        form = AcceptTransactionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            sender_address = data['sender_address']
            recipient_address = data['recipient_address']
            amount_to_receive = data['amount_to_receive']
            signature = data['signature']

            required_values = [sender_address=='', recipient_address=='', amount_to_receive=='', signature=='']
            if any(required_values):
                return HttpResponseBadRequest("Missing values", status=400)

            # create new transaction
            transaction_result = BLOCKCHAIN.submit_transaction(sender_address, recipient_address, amount_to_receive, signature)
            if transaction_result == False:
                response = {'message': 'Invalid Transaction!'}
                return JsonResponse(response, status=406)
            else:
                response = {'message': 'Transaction will be added to Block '+ str(transaction_result)}
                return JsonResponse(response, status=201)
        else:
            return render(request, template, {'form' : form})
    return render(request, template, {'form' : AcceptTransactionForm()})

def transactions_in_block(request):
    """Get list of transactions in a block"""
    template = 'chain/get_transactions.html'
    context = {}
    context['transactions'] = BLOCKCHAIN.transactions
    return render(request, template, context)
    # return JsonResponse(context, status=200)

def chain(request):
    template = 'chain/chain.html'
    chain = BLOCKCHAIN.chain
    context = {}
    context['chain'] = chain
    context['chain_length'] = len(chain)
    return render(request, template, context)

def mine(request):
    template = 'chain/mine.html'
    context = {}
    # get next proof from POW algorithm
    last_block = BLOCKCHAIN.chain[-1]
    nonce = BLOCKCHAIN.proof_of_work()

    # reward for finding proof
    BLOCKCHAIN.submit_transaction(sender_address=MINING_SENDER, recipient_address=BLOCKCHAIN.node_id, value=MINING_REWARD, signature="")

    # forge new block and add to chain
    previous_hash = BLOCKCHAIN.hash(last_block)
    block = BLOCKCHAIN.create_block_and_add_to_chain(nonce, previous_hash)

    context['message'] = "New block forged and added to chain"
    context['block_number'] = block['block_number']
    context['transactions'] = block['transactions']
    context['nonce'] = block['nonce']
    context['previous_hash'] = block['previous_hash']

    return render(request, template, context)

def register_nodes(request):
    """Register a new node"""
    template = 'chain/node_register.html'
    context = {}

    if request.method == 'POST':
        form = NodeRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            node_urls = data['node_urls']

            for node_url in node_urls:
                BLOCKCHAIN.register_node(node_url)
            msg = "New nodes have been added"
            messages.success(request, msg)
            return redirect('blockchain:node_index')
        else:
            return render(request, template, {'form' : form})
    return render(request, template, {'form' : NodeRegistrationForm()})

def node_index(request):
    template = 'chain/node_index.html'
    context = {}
    context['nodes'] = BLOCKCHAIN.nodes
    return render(request, template, context)

def consensus(request):
    template = 'chain/nodes_resolve.html'
    context = {}
    replaced = BLOCKCHAIN.resolve_conflicts()

    if replaced:
        msg = 'Our chain was replaced'
        context['msg'] = msg
        context['chain'] = BLOCKCHAIN.chain
        messages.error(request, msg)
    else:
        msg = 'Our chain was preferred'
        context['msg'] = msg
        context['chain'] = BLOCKCHAIN.chain
        messages.success(request, msg)
    # return redirect('blockchain:node_index')
    return render(request, template, context)

