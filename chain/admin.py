from django.contrib import admin

from .models import BlockAccount

class BlockAccountAdmin(admin.ModelAdmin):
    list_display = ('owner', 'alias', 'used', 'balance', 'private_key', 'public_key')

admin.site.register(BlockAccount, BlockAccountAdmin)
