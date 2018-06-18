"""Admin"""

from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser, SiteUser, Wallet
from .forms import UserChangeForm, UserCreationForm

class SiteUserAdmin(admin.ModelAdmin):
    list_display = ("screen_name", "user", "slug")

class WalletAdmin(admin.ModelAdmin):
    list_display = ('owner', 'alias', 'used', 'balance', 'private_key', 'public_key')

admin.site.register(Wallet, WalletAdmin)

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_admin', 'is_active', "prof")
    list_filter = ('is_admin', )
    fieldsets = (
        (None, {'fields' : ('email', 'password')}),
        ('Personal info', {'fields' : ()}),
        ('Permissions', {'fields' : ('is_admin', 'is_active')})
    )

    add_fieldsets = (
        (None, {
            'classes' : ('wide', ),
            'fields' : ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', )
    ordering = ('email', )
    filter_horizontal = ()

admin.site.register(SiteUser, SiteUserAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Permission)

admin.site.unregister(Group)
