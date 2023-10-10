from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class FlaskAPITokenBackend(BaseBackend):
    def authenticate(self, request, token=None):
        if token is None:
            token = request.session.get('access_token')
        
        if token:
            try:
                # Use the Token model to check the validity of the access token
                token_obj = Token.objects.get(key=token)
                return token_obj.user
            except Token.DoesNotExist:
                pass  # Invalid token

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
