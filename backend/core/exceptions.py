from rest_framework import status


class ServiceError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class BadRequestError(ServiceError):
    status_code = status.HTTP_400_BAD_REQUEST


class TooManyRequestsError(ServiceError):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS