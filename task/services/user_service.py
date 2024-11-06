from django.contrib.auth.models import User, UserManager
from rest_framework.authtoken.models import Token

from task.exceptions.task_exceptions import UnhandledProcessTaskTransaction


class UserServices(UserManager):

    def __init__(self):
        pass

    def logout_user(self, user: User):
        self.__logout_user(user)

    @staticmethod
    def __logout_user(user: User):
        try:
            token = Token.objects.get(user=user)
            token.delete()
        except Exception as error:
            raise UnhandledProcessTaskTransaction(error)