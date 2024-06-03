from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
class User(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    language = models.CharField(max_length=10, default='en', choices=(
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
    ))
    is_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=60,blank=True, null=True)
    last_name = models.CharField(max_length=60,blank=True, null=True)
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

class OTPVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_codes')
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

class PaymentMethod(models.Model):
    CREDIT_CARD = 'credit_card'
    BANK_ACCOUNT = 'bank_account'
    PAYPAL = 'paypal'
    OTHER = 'other'
    
    PAYMENT_CHOICES = [
        (CREDIT_CARD, 'Credit Card'),
        (BANK_ACCOUNT, 'Bank Account'),
        (PAYPAL, 'PayPal'),
        (OTHER, 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    method_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default=BANK_ACCOUNT)
    details = models.CharField(max_length=255)

class Transaction(models.Model):
    TYPE_CHOICES = (
        ('send', 'Send Money'),
        ('receive', 'Receive Money'),
    )

    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=50, choices=TYPE_CHOICES)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    details = models.TextField()
    issued_on = models.DateTimeField(auto_now_add=True)

class QRCodePayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qr_payments')
    qr_code = models.ImageField(upload_to='qr_codes/')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class KYC(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kyc_documents')
    name = models.CharField(max_length=255, null=True, blank=True)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    cnic_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    cnic_issue_date = models.DateField(null=True, blank=True)
    cnic_expiry_date = models.DateField(null=True, blank=True)
    cnic_picture = models.ImageField(upload_to='kyc_docs/cnic_pictures/', null=True, blank=True)
    user_selfie = models.ImageField(upload_to='kyc_docs/user_selfies/', null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.cnic_number}"

class BillPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bill_payments')
    bill_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateTimeField(auto_now_add=True)

