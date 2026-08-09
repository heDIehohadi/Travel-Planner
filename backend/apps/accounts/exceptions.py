class OTPError(Exception):
    pass
class OTPNotFound(OTPError):
    pass
class InvalidOTPError(OTPError):
    pass
class ExpiredOTPError(OTPError):
    pass
class TooManyAttemptsError(OTPError):
    pass
class RateLimitError(OTPError):
    pass