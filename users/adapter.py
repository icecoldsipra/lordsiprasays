"""
from allauth.account.adapter import DefaultAccountAdapter
# from django.contrib import messages


class AccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):

        return "/"
"""
