from rest_framework import serializers
# We use Serializer because this endpoint performs an action
# (requesting an OTP) instead of creating/updating a model directly.

class RequestOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

class VerifyOTPSerializer(serializers.Serializer):
    phone_number=serializers.CharField()
    otp_code=serializers.CharField()    