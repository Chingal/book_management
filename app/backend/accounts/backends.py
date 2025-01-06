from django.contrib.auth.backends import BaseBackend

class NoAuthBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        return None

    def get_user(self, user_id):
        return None
