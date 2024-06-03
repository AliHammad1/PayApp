from rest_framework import viewsets, status, views
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from .serializers import (KYCUploadCNICPictureSerializer, KYCUploadSelfieSerializer, SignUpUserSerializer, UserSerializer, UserProfileSerializer, OTPVerificationSerializer,
                          PaymentMethodSerializer, TransactionSerializer, NotificationSerializer,
                          InvoiceSerializer, QRCodePaymentSerializer, KYCSerializer, BillPaymentSerializer, UserSerializerP)
from .models import UserProfile, OTPVerification, PaymentMethod, Transaction, Notification, Invoice, QRCodePayment, KYC, BillPayment
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework.mixins import CreateModelMixin ,RetrieveModelMixin
from rest_framework.decorators import action
User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpUserSerializer

    @action(detail=False, methods=['post'], url_path='signup')
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SignInView(views.APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        print("Attempting to authenticate:", username, password)
        user = authenticate(request, username=username, password=password)
        if user:
            print("Authentication successful for user:", username)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            print("Authentication failed for user:", username)
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
class UserListView(views.APIView):
   

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializerP(users, many=True)
        return Response(serializer.data)

class OTPVerificationViewSet(viewsets.ModelViewSet):
    queryset = OTPVerification.objects.all()
    serializer_class = OTPVerificationSerializer

class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class QRCodePaymentViewSet(viewsets.ModelViewSet):
    queryset = QRCodePayment.objects.all()
    serializer_class = QRCodePaymentSerializer



class BillPaymentViewSet(viewsets.ModelViewSet):
    queryset = BillPayment.objects.all()
    serializer_class = BillPaymentSerializer

class SignUpView(views.APIView):
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignInView(views.APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     logout(request)
    #     return Response({"message": "Successfully logged out"}, status=status.HTTP_204_NO_CONTENT)
    
class SubmitSelfieView(CreateModelMixin, viewsets.GenericViewSet):
    queryset = KYC.objects.all()
    serializer_class = KYCUploadSelfieSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        kyc, created = KYC.objects.get_or_create(user=user)
        serializer = self.get_serializer(kyc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubmitCNICPictureView(CreateModelMixin, viewsets.GenericViewSet):
    queryset = KYC.objects.all()
    serializer_class = KYCUploadCNICPictureSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            kyc = KYC.objects.get(user=user)
        except KYC.DoesNotExist:
            return Response({"error": "KYC record not found. Please submit selfie first."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(kyc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubmitKYCFormView(CreateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = KYC.objects.all()
    serializer_class = KYCSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            kyc = KYC.objects.get(user=user)
            # If KYC record exists, update it
            serializer = self.get_serializer(kyc, data=request.data)
        except KYC.DoesNotExist:
            # If KYC record does not exist, create a new one
            serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=user)  # Ensure user is associated with KYC
            return Response(serializer.data, status=status.HTTP_200_OK if kyc else status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            kyc = KYC.objects.get(user=user)
            serializer = self.get_serializer(kyc)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except KYC.DoesNotExist:
            return Response({"error": "KYC data not found."}, status=status.HTTP_404_NOT_FOUND)