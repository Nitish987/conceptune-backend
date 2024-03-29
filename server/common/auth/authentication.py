from rest_framework import authentication
from rest_framework import exceptions
from app.account.models import User
from .jwt_token import Jwt
from constants.tokens import TokenType, HeaderToken
from constants.headers import Header
from ..debug.log import Log


# User Authentication
class UserAuthentication(authentication.BaseAuthentication):
    '''Authenticate user through Jwt Access Token.'''

    def authenticate(self, request):
        try:
            # getting validation success and payload from authentication token
            bearer_token = request.META.get(HeaderToken.ACCESS_TOKEN).split(' ')[1]
            success, payload = Jwt.validate(bearer_token)
        
            # validating authentication token
            if not success or payload['type'] != TokenType.LOGIN or payload['sub'] != request.META.get(Header.USER_ID):
                return None

            try:
                # fetching user from database
                user = User.objects.get(uid=payload['sub'])
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed('No such Account found.')

            return (user, None)
        except:
            return None
