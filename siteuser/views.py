
"""Views"""

import uuid
import operator
from functools import reduce

from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views import generic
from django.shortcuts import render, reverse, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from pure_pagination.mixins import PaginationMixin
from social_django.models import UserSocialAuth

from .models import SiteUser

from .forms import (PassWordGetterForm, EmailAndPassWordGetterForm,
    SiteUserRegistrationForm, SiteUserEditForm
)
from .utils import check_recaptcha

CustomUser = get_user_model()

class SiteUserIndex(PaginationMixin, generic.ListView):
    model = SiteUser
    context_object_name = 'siteuser_list'
    template_name = "siteuser/index.html"
    paginate_by = 20

class SiteUserCommonLocation(PaginationMixin, generic.ListView):
    model = SiteUser
    context_object_name = 'siteuser_list'
    template_name = "siteuser/siteuser_common_location.html"
    paginate_by = 20

    def get_queryset(self):
        locations = self.kwargs['location'].split(" ")
        query = []
        for each in locations:
            query.append(Q(location__contains=each))
        query = reduce(operator.or_, query)
        return SiteUser.objects.filter(query)

    def get_context_data(self, *args):
        context = super(SiteUserCommonLocation, self).get_context_data(*args)
        context['location'] = self.kwargs['location']
        return context

@check_recaptcha
def new_siteuser(request):
    template = "siteuser/new.html"
    if request.method == 'POST':
        form = SiteUserRegistrationForm(request.POST)
        if form.is_valid() and request.recaptcha_is_valid:
            form = form.cleaned_data
            email = form['email']
            screen_name = form['screen_name']
            password1 = form['password1']

            user = CustomUser(email=email)
            user.set_password(password1)
            user.save()

            new_user = SiteUser(user=user, screen_name=screen_name)
            new_user.save()

            # 2. send email
            activation_link = request.build_absolute_uri(new_user.get_user_creation_url())
            screen_name = new_user.screen_name
            context = {'screen_name' : screen_name, 'activation_link' : activation_link}

            subject = "Welcome to Blockchain {}.".format(screen_name)
            from_email = settings.EMAIL_HOST_USER

            text_email = render_to_string("welcome_email_template.txt", context)
            html_email = render_to_string("welcome_email_template.html", context)

            for each in [email, "choralcentral@gmail.com"]:
                msg = EmailMultiAlternatives(subject, text_email, from_email, [each])
                msg.attach_alternative(html_email, "text/html")
                msg.send()
            return redirect(reverse('siteuser:new_success', args=[screen_name]))
        else:
            return render(request, template, {'form' : form})
    return render(request, template, {'form' : SiteUserRegistrationForm()})

def welcome_siteuser(request, screen_name):
    template = 'siteuser/new_success.html'
    context = {'screen_name' : screen_name}
    return render(request, template, context)

def activate_siteuser(request, screen_name, pk):
    # check time to see if link has expired.
    user = CustomUser.objects.get(pk=pk)
    context = {}
    if user.is_active:
        siteuser = SiteUser.objects.get(user=user)
        context["active"] = "active"
        context["siteuser"] = siteuser
    else:
        user.is_active = True
        user.save()
        siteuser = SiteUser.objects.get(user=user)
        context["siteuser"] = siteuser
    context["screen_name"] = screen_name
    return render(request, "siteuser/new_activation.html", context)

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

def deactivate_account(request):
    template = 'siteuser/deactivate_account.html'
    user = request.user
    if request.method == 'POST':
        form = PassWordGetterForm(request.POST, user=user)
        if form.is_valid():
            user.is_active = False
            user.save()
            msg = "Your account has been deactivated"
            messages.success(request, msg)
            return redirect('/')
        else:
            # return render(request, template, {'form' : form })
            msg = "You entered a wrong password"
            messages.error(request, msg)
            return redirect('/')
    return render(request, template, {'form' : PassWordGetterForm(user=user) })

# complete later
def activate_account(request):
    template = 'siteuser/activate_account.html'
    if request.method == 'POST':
        form = EmailAndPassWordGetterForm(request.POST)
        if form.is_valid():
            user.is_active = False
            user.save()
            msg = "Your account has been deactivated"
            messages.success(request, msg)
            return redirect('/')
        else:
            msg = "You entered a wrong password"
            messages.error(request, msg)
            return redirect('/')
    return render(request, template, {'form' : PassWordGetterForm(user=user) })

@login_required
def account_management(request):
    template = "siteuser/account_management.html"
    context = {}
    user = request.user
    siteuser = user.siteuser

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    try:
        google_login = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        yahoo_login = user.social_auth.get(provider='yahoo-oauth2')
    except UserSocialAuth.DoesNotExist:
        yahoo_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    context['siteuser'] = siteuser
    context['facebook_login'] = facebook_login
    context['google_login'] = google_login
    context['twitter_login'] = twitter_login
    context['yahoo_login'] = yahoo_login
    context['can_disconnect'] = can_disconnect
    return render(request, template, context)

@login_required
def social_password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            login(request, request.user, backend='django.contrib.auth.backends.ModelBackend',)
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'siteuser/social_password_change_form.html', {'form': form})

