from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @staticmethod
    def _build_response(success: bool, response_code: str, status_code, data: dict | None = None) -> Response:
        response_data = {
            'success': success,
            'data': data,
            'response_code': response_code
        }
        return Response(
            status=status_code,
            data=response_data,
        )

    @staticmethod
    def _build_list_response(
            success: bool,
            response_code: str,
            total_page: int,
            status_code,
            data: dict | None = None
    ) -> Response:
        response_data = {
            'success': success,
            'data': data,
            'response_code': response_code,
            'total_page': total_page,
        }
        return Response(
            status=status_code,
            data=response_data
        )
