from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import UserRegistration

class UserRegistrationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            try:
                user_registration = UserRegistration.objects.get(user__username=username)
                if user_registration.user.check_password(password):
                    user = user_registration.user
                    return user
            except UserRegistration.DoesNotExist:
                return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
