from django.conf import settings
from rest_framework import permissions
from django.core.cache import cache
from constants.tokens import HeaderToken, TokenType
from constants.headers import Header
from .jwt_token import Jwt


# Api Request valid permission
class IsRequestValid(permissions.BasePermission):
    def has_permission(self, request, view):
        key = request.META.get(Header.APP_API_KEY)
        return key == settings.APP_API_KEY



# Account Creation valid permission
class IsAccountCreationKeyValid(permissions.BasePermission):
    def has_permission(self, request, view):
        key = request.META.get(Header.ACCOUNT_CREATION_KEY)
        return key == settings.ACCOUNT_CREATION_KEY



# User Account Identity Token Session valid permission
class IsIdentitySessionValid(permissions.BasePermission):
    def has_permission(self, request, view):
        idt = request.META.get(HeaderToken.IDENTITY_TOKEN)
        is_valid, payload = Jwt.validate(idt)
        return is_valid and payload['type'] == TokenType.IDENTITY and payload['data']['username'] == request.user.username