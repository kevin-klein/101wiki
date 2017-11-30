from django.contrib.auth.backends import ModelBackend
from .models import User


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password.

    """
    def authenticate(self, username=None):
        try:
            return User.objects.get(name=username)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        print(user_id)
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
