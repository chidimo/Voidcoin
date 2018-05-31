from django.db.models import Sum
from django.shortcuts import render, redirect
from django.http import  JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import binascii
import Crypto.Random
# from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

from .blockchain_client import Transaction, COINBASE, MINING_DIFFICULTY, MINING_REWARD, MINABLE_TRANSACTIONS
from .forms import InitiateTransactionForm, InitiateTransactionAuthUserForm, NodeRegistrationForm, EditAliasForm

from .models import Wallet

# Instantiate a blockchain
BLOCKCHAIN = settings.BLOCKCHAIN

def index(request):
    # get balance of coins in the system
    SUM_COINS = Wallet.objects.aggregate(total_balance=Sum('balance'))['total_balance']
    # If no wallet instance has been created, the balance returns None
    if SUM_COINS == None:
        SUM_COINS = 0.00
    template = 'chain/index.html'
    context = {}
    context['pending_transactions'] = BLOCKCHAIN.transactions
    context['chain'] = BLOCKCHAIN.chain
    context['mining_difficulty'] = MINING_DIFFICULTY
    context['mining_reward'] = MINING_REWARD
    context['coin_base'] = COINBASE
    context['unassigned'] = COINBASE - SUM_COINS
    context['mineable'] = MINABLE_TRANSACTIONS
    return render(request, template, context)

def generate_wallet(request):
    """Generate a new wallet"""
    random_gen = Crypto.Random.new().read
    pr_key = RSA.generate(1024, random_gen)
    pub_key = pr_key.publickey()

    private_key = binascii.hexlify(pr_key.exportKey(format='DER')).decode('ascii')
    public_key = binascii.hexlify(pub_key.exportKey(format='DER')).decode('ascii')

    # get balance of coins in the system
    SUM_COINS = Wallet.objects.aggregate(total_balance=Sum('balance'))['total_balance']
    # If no wallet instance has been created, the balance returns None
    if SUM_COINS == None:
        SUM_COINS = 0.00
    if SUM_COINS < COINBASE:
        balance = 50.00
    else:
        balance = 0.00

    messages.success(request, "New wallet generated successfully.")
    messages.success(request, "You have been assigned an initial coin balance of {}".format(balance))
    if request.user.is_authenticated is False:
        messages.error(request, "Copy your public and private keys and save them in a safe place at once as they cannot be recovered if lost")
        messages.success(request, "Public key: {}".format(public_key))
        messages.success(request, "Private key: {}".format(private_key))
        return redirect('blockchain:index')
    else:
        messages.success(request, "You can view your account keys from your dashboard")
        # save credentials to database
        Wallet.objects.create(alias="Rename (30 characters)",
            owner=request.user.siteuser, private_key=private_key, balance=balance, public_key=public_key)
        return redirect('siteuser:account_management')

def transactions_index(request):
    """View all transactions on the blockchain"""
    template = 'chain/transactions_index.html'
    context = {}
    context['transactions'] = [transaction for block in BLOCKCHAIN.chain for transaction in block['transactions']]
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
        form = InitiateTransactionAuthUserForm(request.POST, user=user)
        if form.is_valid():
            data = form.cleaned_data
            wallet = data['wallet']
            recipient = data['recipient']
            amount_to_send = data['amount_to_send']

            sender_address = wallet.public_key
            sender_private_key = wallet.private_key
            recipient_address = recipient.public_key

            transaction_object = Transaction(sender_address, sender_private_key, recipient_address, amount_to_send)
            transaction = transaction_object.to_dict()
            signature = transaction_object.sign_transaction()
            verify = BLOCKCHAIN.verify_transaction_signature(sender_address, signature, transaction)
            if verify:
                BLOCKCHAIN.add_transaction_to_current_array(sender_address, recipient_address, amount_to_send, signature)
                messages.success(request, "Transaction signature verified successfully and transaction stacked for 'blocking'.")
            else:
                messages.error(request, "Transaction rejected")

            # update wallet balances
            wallet.balance -= amount_to_send
            wallet.save()
            recipient.balance += amount_to_send
            recipient.save()

            return redirect('blockchain:transactions_destined_for_next_block')
        else:
            return render(request, template, {'form' : form})
    return render(request, template, {'form' : InitiateTransactionAuthUserForm(user=user)})

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

def block_detail(request, index):
    """View transactions in a block"""
    template = 'chain/block_detail.html'
    context = {}
    number = int(index)-1
    context['number'] = number + 1
    context['block_items'] = BLOCKCHAIN.chain[number]
    return render(request, template, context)

def mine(request):
    if BLOCKCHAIN.mineable() is False:
        messages.error(request, "At least three (3) transactions are needed to forge a block.")
        return redirect('blockchain:index')

    # get next proof from POW algorithm
    last_block = BLOCKCHAIN.last_block()
    nonce = BLOCKCHAIN.proof_of_work()

    # reward for finding proof
    BLOCKCHAIN.reward_miner(BLOCKCHAIN.node_id)

    # forge new block and add to chain
    previous_hash = BLOCKCHAIN.hash(last_block)
    BLOCKCHAIN.forge_block_and_add_to_chain(nonce, previous_hash)
    messages.success(request, "Block mined successfully")
    messages.success(request, "You have been rewarded with 0.25 coins")
    return redirect('blockchain:index')

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

def edit_alias(request):
    user = request.user
    template = 'chain/edit_alias.html'

    if request.method == 'POST':
        form = EditAliasForm(request.POST, user=user)
        if form.is_valid():
            data = form.cleaned_data
            alias = data['alias']
            account = data['account']

            account.alias = alias
            account.save(update_fields=['alias'])
            messages.success(request, "Wallet alias updated successfully")
            return redirect('siteuser:account_management')
        else:
            return render(request, template, {'form' : form})
    return render(request, template, {'form' : EditAliasForm(user=user)})

def wallet_index(request):
    template = 'chain/wallet_index.html'
    context = {}
    context['wallets'] = Wallet.objects.all()
    return render(request, template, context)
