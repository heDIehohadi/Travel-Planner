from .otp_service import OTPService
from apps.accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class AuthenticationService:

    def authenticate_with_otp(self, phone_number, otp_code):
        otp_service = OTPService()
        otp_service.verify_otp(phone_number, otp_code)

        user, created = User.objects.get_or_create(
            phone_number=phone_number
        )

        user.is_phone_verified = True
        user.save(update_fields=["is_phone_verified"])

        refresh = RefreshToken.for_user(user)#ask to create a refreshtoken for user
        access = refresh.access_token

        return {
            "access": str(access),
            "refresh": str(refresh),
        }