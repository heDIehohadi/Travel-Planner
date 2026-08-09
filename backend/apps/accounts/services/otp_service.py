from datetime import timedelta  # use for a extra minuts to  add time
import secrets  # use for random code which are(token,otpcode,authentication,..)
from django.db import transaction  # for action we need to done all or stop all
# better use it as decorator, not with (with statement)
from django.utils import timezone  # for django timezone is better
from apps.accounts.models import OTPRequest
from accounts.exceptions import ExpiredOTPError,InvalidOTPError,TooManyAttemptsError,RateLimitError,OTPNotFound

class OTPService:
    """otp lifecycle"""

    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 2
    MAX_VERIFY_ATTEMPTS = 5  # do not use magic number in production
    RESEND_COOLDOWN_SECONDS = 60  # minimum time user must wait before requesting a new otp

    def _create_otp_code(self):
        """create the code"""
        code = secrets.randbelow(10 ** self.OTP_LENGTH)  # randbelow has a [0,n) range
        return str(code).zfill(self.OTP_LENGTH)  # randbelow has a random length so we need 6 length
        # we use zfill(length_number) and make a intcode to str

    def _invalidate_previous_otps(self, phone_number):
        """expire the previous code"""
        OTPRequest.objects.filter(
            phone_number=phone_number,
            is_used=False,
        ).update(is_used=True)  # update: change many records at the same time

    def _check_rate_limit(self, phone_number):
        """block a new otp request if the last one was too recent"""
        last_otp = (
            OTPRequest.objects
            .filter(phone_number=phone_number)
            .order_by("-created_at")
            .first()  # get the most recent otp for this phone number
        )

        if last_otp is None:
            return  # no previous otp, nothing to rate limit against

        seconds_since_last = (timezone.now() - last_otp.created_at).total_seconds()

        if seconds_since_last < self.RESEND_COOLDOWN_SECONDS:
            wait_time = int(self.RESEND_COOLDOWN_SECONDS - seconds_since_last)
            raise RateLimitError(f"please try a {wait_time}seconds")

    @transaction.atomic  # in the below method the operations are consecutive
    def generate_otp(self, phone_number):

        self._check_rate_limit(phone_number)  # must run before invalidating/creating anything
        self._invalidate_previous_otps(phone_number)
        otp_code = self._create_otp_code()
        expires_at = timezone.now() + timedelta(
            minutes=self.OTP_EXPIRY_MINUTES
        )

        otp = OTPRequest.objects.create(phone_number=phone_number,otp_code=otp_code,
            expires_at=expires_at,)

        return otp

    def verify_otp(self, phone_number, otp_code):

        otp = OTPRequest.objects.filter(
            phone_number=phone_number,
            is_used=False,
        ).first()  # return the first member of the record

        if otp is None:

            raise OTPNotFound("OTP not found.")

        if otp.expires_at < timezone.now():
            otp.is_used = True
            otp.save(update_fields=["is_used"])  # save is just for one obj

            raise ExpiredOTPError("OTP expired")

        if otp.attempts >= self.MAX_VERIFY_ATTEMPTS:
            otp.is_used = True
            otp.save(update_fields=["is_used"])  # update_fields limits which model fields are updated in database

            raise TooManyAttemptsError(
                "limit attemps,please request new code"
            )

        if otp.otp_code != otp_code:
            otp.attempts += 1
            otp.save(update_fields=["attempts"])

            raise InvalidOTPError("invalid OTP")

        otp.is_used = True
        otp.save(update_fields=["is_used"])

        return True