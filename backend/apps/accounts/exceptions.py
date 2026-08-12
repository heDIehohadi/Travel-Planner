from core.exceptions import BadRequestError, TooManyRequestsError


class OTPNotFound(BadRequestError):
    pass

class InvalidOTPError(BadRequestError):
    pass

class ExpiredOTPError(BadRequestError):
    pass

class TooManyAttemptsError(TooManyRequestsError):
    pass

class RateLimitError(TooManyRequestsError): pass
