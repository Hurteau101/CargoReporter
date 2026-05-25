# authentication/adapter.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponseForbidden

from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import render
from authentication.models import AllowedEmail


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email', '')
        if not AllowedEmail.objects.filter(email__iexact=email).exists():
            response = render(request, '403.html', status=403)
            raise ImmediateHttpResponse(response)
