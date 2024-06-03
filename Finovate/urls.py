# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (SubmitCNICPictureView, SubmitKYCFormView, SubmitSelfieView, UserListView, UserProfileViewSet, OTPVerificationViewSet, PaymentMethodViewSet,
                    TransactionViewSet, NotificationViewSet, InvoiceViewSet, QRCodePaymentViewSet,
                     BillPaymentViewSet, SignUpView, SignInView, UserViewSet)

router = DefaultRouter()

router.register(r'user_profiles', UserProfileViewSet)
router.register(r'otp_verifications', OTPVerificationViewSet)
router.register(r'payment_methods', PaymentMethodViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'qr_code_payments', QRCodePaymentViewSet)

router.register(r'bill_payments', BillPaymentViewSet)
router.register(r'submit-selfie', SubmitSelfieView, basename='submit-selfie')
router.register(r'submit-cnic-picture', SubmitCNICPictureView, basename='submit-cnic-picture')
router.register(r'submit-kyc-form', SubmitKYCFormView, basename='submit-kyc-form')
router.register(r'signup', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('signin/', SignInView.as_view(), name='signin'),
    # path('submit-selfie/', SubmitSelfieView.as_view(), name='submit_selfie'),
    # path('submit-cnic-picture/', SubmitCNICPictureView.as_view(), name='submit_cnic_picture'),
    # path('submit-kyc-form/', SubmitKYCFormView.as_view(), name='submit_kyc_form'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('kyc/<int:user_id>/', SubmitKYCFormView.as_view({'get': 'retrieve', 'post': 'create'})),
]
