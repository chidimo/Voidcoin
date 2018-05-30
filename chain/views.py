from decimal import Decimal

from django.db.models import Sum
from django.shortcuts import render, redirect
from django.http import  JsonResponse, HttpResponseBadRequest#, HttpResponse
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.conf import settings
from django.contrib import messages
# from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

import binascii
import Crypto.Random
# from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

from .blockchain_client import Transaction, Blockchain, MINING_SENDER, MINING_REWARD, COINBASE
from .forms import InitiateTransactionForm, InitiateTransactionChoiceFieldForm, AcceptTransactionForm, NodeRegistrationForm, EditIdentifyForm

from .models import BlockAccount

# Instantiate a blockchain
BLOCKCHAIN = Blockchain()

def index(request):
    template = 'chain/index.html'
    context = {}
    context['blockchain'] = BLOCKCHAIN
    return render(request, template, context)

def generate_wallet(request):
    """Generate a new wallet"""
    random_gen = Crypto.Random.new().read
    pr_key = RSA.generate(1024, random_gen)
    pub_key = pr_key.publickey()

    private_key = binascii.hexlify(pr_key.exportKey(format='DER')).decode('ascii')
    public_key = binascii.hexlify(pub_key.exportKey(format='DER')).decode('ascii')

    context = {'private_key' : private_key,'public_key' : public_key}
    messages.success(request, "New wallet generated successfully")
    messages.warning(request, "Save keys in a safe place at once as they cannot be recovered if lost")

    # get balance of coins in the system
    sum_coins = BlockAccount.objects.aggregate(total_balance=Sum('balance'))['total_balance']

    # If no instance has been created, the balance is None
    if sum_coins == None:
        sum_coins = Decimal('0.00')
    if sum_coins < COINBASE:
        balance = Decimal('10.00')
    else:
        balance = Decimal('0.00')

    # save credentials to database
    BlockAccount.objects.create(
        owner=request.user.siteuser, private_key=private_key, balance=balance, public_key=public_key)

    return redirect('siteuser:account_management')

def transactions_index(request):
    """View all transactions on the blockchain"""
    template = 'chain/transactions_index.html'
    context = {}
    context['blockchain_transactions'] = [transaction for block in BLOCKCHAIN.chain for transaction in block.transactions]
    context['blockchain'] = BLOCKCHAIN
    return render(request, template, context)

def transactions_destined_for_next_block(request):
    """View all transactions to be added to the next block"""
    template = 'chain/transactions_destined_for_next_block.html'
    context = {}
    context['transactions'] = BLOCKCHAIN.transactions
    return render(request, template, context)

@login_required
def transaction_auth_user(request):
    """
    Initiate a transaction and send it to a blockchain node
    """
    user = request.user
    template = 'chain/initiate_transaction.html'

    if request.method == 'POST':
        form = InitiateTransactionChoiceFieldForm(request.POST, user=user)
        if form.is_valid():
            data = form.cleaned_data
            sender = data['sender']
            recipient = data['recipient']
            amount_to_send = data['amount_to_send']

            sender_address = sender.public_key
            sender_private_key = sender.private_key
            recipient_address = recipient.public_key

            transaction_object = Transaction(sender_address, sender_private_key, recipient_address, amount_to_send)
            transaction = transaction_object.to_dict()
            signature = transaction_object.sign_transaction()
            verify = BLOCKCHAIN.verify_transaction_signature(sender_address, signature, transaction)
            if verify:
                BLOCKCHAIN.add_transaction_to_current_array(sender_address, recipient_address, amount_to_send, signature)
                messages.success(request, "Transaction signature verified successfully")
            else:
                messages.error(request, "Transaction rejected")
            return redirect('siteuser:account_management')
        else:
            return render(request, template, {'form' : form})
    return render(request, template, {'form' : InitiateTransactionChoiceFieldForm(user=user)})

def transaction_anon(request):
    """
    Initiate a transaction and send it to a blockchain node
    """
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

            transaction_object = Transaction(sender_address, sender_private_key, recipient_address, amount_to_send)
            context['transaction'] = transaction_object.to_dict()
            context['signature'] = transaction_object.sign_transaction()
            return JsonResponse(context, status=201)
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

            required_values = [sender_address=='', recipient_address=='', amount_to_receive==None, signature=='']
            if any(required_values):
                return HttpResponseBadRequest("Missing values", status=400)

            # create new transaction
            transaction_result = BLOCKCHAIN.add_transaction_to_current_array(sender_address, recipient_address, amount_to_receive, signature)
            if transaction_result == False:
                context = {'message': 'Invalid Transaction!'}
                return JsonResponse(context, status=406)
            else:
                context = {'message': 'Transaction will be added to Block '+ str(transaction_result)}
                return JsonResponse(context, status=201)
        else:
            return render(request, template, {'form' : form})
    return render(request, template, {'form' : AcceptTransactionForm()})

def block_detail(request, index):
    """Get list of transactions in a block"""
    template = 'chain/get_transactions.html'
    context = {}
    block = BLOCKCHAIN.chain[index]
    context['block'] = block
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
    BLOCKCHAIN.add_transaction_to_current_array(sender_address=MINING_SENDER, recipient_address=BLOCKCHAIN.node_id, amount=MINING_REWARD, signature="")

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
    """Register new nodes"""
    template = 'chain/node_register.html'

    if request.method == 'POST':
        form = NodeRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            node_urls = data['node_urls'].split(',')

            for node_url in node_urls:
                try:
                    BLOCKCHAIN.register_node(node_url)
                    continue
                except ValueError:
                    messages.error(request, "Invalid node url: {}".format(node_url))
                    return redirect('blockchain:node_index')
            messages.success(request, "Node urls added successfully")
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

def edit_identify(request):
    user = request.user
    template = 'chain/edit_identify.html'

    if request.method == 'POST':
        form = EditIdentifyForm(request.POST, user=user)
        if form.is_valid():
            data = form.cleaned_data
            identify = data['identify']
            account = data['account']

            account.identify = identify
            account.save(update_fields=['identify'])
            messages.success(request, "Key identifier updated successfully")
            return redirect('siteuser:account_management')
        else:
            return render(request, template, {'form' : form})
    return render(request, template, {'form' : EditIdentifyForm(user=user)})

