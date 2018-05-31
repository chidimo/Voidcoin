from django.contrib import admin

from .models import Wallet

class WalletAdmin(admin.ModelAdmin):
    list_display = ('owner', 'alias', 'used', 'balance', 'private_key', 'public_key')

admin.site.register(Wallet, WalletAdmin)
