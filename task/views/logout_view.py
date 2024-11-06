from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from customore.base_api_view import BaseAPIView
from task.enums.response_code import ResponseCode
from task.exceptions.task_exceptions import UnhandledProcessTaskTransaction
from task.services.user_service import UserServices


class LogOutView(BaseAPIView):
    authentication_classes = [TokenAuthentication]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UserServices()

    def post(self, request):
        try:
            self.service.logout_user(request.user)
            return self._build_response(
                success=True,
                response_code=ResponseCode.SUCCESS,
                status_code=status.HTTP_200_OK,
            )
        except UnhandledProcessTaskTransaction:
            return self._build_response(
                success=False,
                response_code=ResponseCode.UNKNOWN_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )