from rest_framework.views import exception_handler
from rest_framework.response import Response

from core.exceptions import ServiceError


def custom_exception_handler(exc, context):
    """
    Convert application exceptions into appropriate HTTP responses.
    """
    response = exception_handler(exc, context)
    if response is not None:
        return response

    if isinstance(exc, ServiceError):
        return Response({"detail": str(exc)}, status=exc.status_code)

    return None