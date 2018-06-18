
"""Views"""

from django.db.models import Sum
from django.views import generic
from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import SiteUser, Wallet
from chain.blockchain_client import Transaction, COINBASE, MINING_DIFFICULTY, MINING_REWARD, MINABLE_TRANSACTIONS

from .forms import PassWordGetterForm, SiteUserRegistrationForm, SiteUserEditForm, EditAliasForm
from django.contrib.auth.decorators import login_required

import binascii
import Crypto.Random
# from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

CustomUser = get_user_model()

def new_siteuser(request):
    template = "siteuser/new.html"
    if request.method == 'POST':
        form = SiteUserRegistrationForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            email = form['email']
            screen_name = form['screen_name']
            password1 = form['password1']

            user = CustomUser(email=email)
            user.set_password(password1)
            user.is_active=True
            user.save()

            new_user = SiteUser(user=user, screen_name=screen_name)
            new_user.save()
            login(request, user)
            return redirect('blockchain:index')
        else:
            return render(request, template, {'form' : form})
    return render(request, template, {'form' : SiteUserRegistrationForm()})

class SiteUserEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = SiteUser
    form_class = SiteUserEditForm
    template_name = 'siteuser/edit.html'
    success_message = "Profile updated successfully."

    def get_object(self):
        user = self.request.user
        return SiteUser.objects.get(pk=user.pk)

    def get_success_url(self):
        return reverse('siteuser:account_management')

def delete_account(request):
    template = 'siteuser/delete_account.html'
    user = request.user
    siteuser = user.siteuser
    if request.method == 'POST':
        form = PassWordGetterForm(request.POST, user=user)
        if form.is_valid():
            siteuser.delete()
            user.delete()
            msg = "Your account has been permanently deleted"
            messages.success(request, msg)
            return redirect('/')
        else:
            # return render(request, template, {'form' : form })
            msg = "You entered a wrong password"
            messages.error(request, msg)
            return redirect('/')
    return render(request, template, {'form' : PassWordGetterForm(user=user) })

@login_required
def account_management(request):
    template = "siteuser/account_management.html"
    context = {}
    context['siteuser'] = request.user.siteuser
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
    messages.success(request, "New wallet generated successfully and you have been assigned an initial coin balance of {}".format(balance))
    if request.user.is_authenticated is False:
        messages.error(request, "Copy your public and private keys and save them in a safe place at once as they cannot be recovered if lost")
        messages.success(request, "PUBLIC KEY: {}\n\nPRIVATE KEY: {}".format(public_key, private_key))
        return redirect('blockchain:index')
    else:
        messages.success(request, "You can view your account keys from your dashboard")
        # save credentials to database
        Wallet.objects.create(alias="Rename (30 characters)",
            owner=request.user.siteuser, private_key=private_key, balance=balance, public_key=public_key)
        return redirect('siteuser:account_management')

def edit_alias(request):
    user = request.user
    template = 'siteuser/wallet_edit_alias.html'

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
    template = 'siteuser/wallet_index.html'
    context = {}
    context['wallets'] = Wallet.objects.all()
    return render(request, template, context)
