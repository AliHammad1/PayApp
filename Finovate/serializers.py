from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile, OTPVerification, PaymentMethod, Transaction, Notification, Invoice, QRCodePayment, KYC, BillPayment
from django.core.validators import RegexValidator

User = get_user_model()

class SignUpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'phone_number', 'language', 'is_verified','first_name','last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', ''),
            language=validated_data.get('language', 'en')
        )
        return user
       
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'language', 'is_verified')

class UserSerializerP(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class OTPVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPVerification
        fields = '__all__'

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class QRCodePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCodePayment
        fields = '__all__'

class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = ['user_id', 'name', 'father_name', 'cnic_number', 'cnic_issue_date', 'cnic_expiry_date']

class KYCUploadSelfieSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = ['user_id','user_selfie']

class KYCUploadCNICPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = ['user_id','cnic_picture']

class BillPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillPayment
        fields = '__all__'
