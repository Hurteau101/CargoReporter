from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import render
from authentication.models import AllowedEmail
from django.shortcuts import redirect

# Ensures that only allowed emails can log in with Google OAuth.
class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email', '')
        if not AllowedEmail.objects.filter(email__iexact=email).exists():
            # response = render(request, 'account/403.html', status=403)
            raise ImmediateHttpResponse(redirect('/access-denied/'))

