from rest_framework.response import Response
from rest_framework.views import APIView


class BaseAPIView(APIView):
    @staticmethod
    def _build_response(success: bool,response_code: str, status_code, data: dict | None = None) -> Response:
        response_data = {
            'success': success,
            'data': data,
            'response_code': response_code
        }
        return Response(
            status=status_code,
            data=response_data
        )