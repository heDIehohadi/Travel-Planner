from rest_framework.views import APIView  # use APIView because OTP endpoints are business actions, not CRUD operations
from rest_framework.response import Response
from apps.accounts.serializer import RequestOTPSerializer, VerifyOTPSerializer

from apps.accounts.services.otp_service import OTPService

class RequestOTPView(APIView):

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        # Create an instance of RequestOTPSerializer and pass incoming request data.
        serializer.is_valid(raise_exception=True)
        # Validate the data and raise an exception automatically if validation fails.
        phone_number = serializer.validated_data["phone_number"]
        # Extract the validated phone number from serializer data.
        otp_service = OTPService()
        # Create an instance of OTPService because generate_otp is an instance method.
        otp_service.generate_otp(phone_number)
        # Generate a new OTP and save it in the database.

        return Response(
            {
                "message": "OTP sent successfully"
            }
        )


class VerifyOTPView(APIView):

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        # Create an instance of VerifyOTPSerializer and pass incoming request data.
        serializer.is_valid(raise_exception=True)
        # Validate the data and raise an exception automatically if validation fails.
        phone_number = serializer.validated_data["phone_number"]
        # Extract the validated phone number from serializer data.
        otp_code = serializer.validated_data["otp_code"]
        # Extract the validated OTP code from serializer data.
        otp_service = OTPService()
        # Create an instance of OTPService because verify_otp is an instance method.
        otp_service.verify_otp(
            phone_number,
            otp_code
        )
        # Verify the OTP code for the given phone number.

        return Response(
            {
                "message": "OTP verified successfully"
            }
        )

    