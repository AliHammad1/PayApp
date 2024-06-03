from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, OTPVerification, PaymentMethod, Transaction, Notification, Invoice, QRCodePayment, KYC, BillPayment
from django.utils.html import format_html

admin.site.register(User)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar_preview']
    readonly_fields = ['avatar_preview']

    def avatar_preview(self, obj):
        from django.utils.html import format_html
        if obj.avatar:
            return format_html('<img src="{}" style="width: 45px; height:45px;" />'.format(obj.avatar.url))
        return "No Image"

admin.site.register(UserProfile, UserProfileAdmin)

class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp', 'created_at']
    search_fields = ['user__username', 'otp']

admin.site.register(OTPVerification, OTPVerificationAdmin)

class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['user', 'method_type', 'details']
    list_filter = ['method_type']

admin.site.register(PaymentMethod, PaymentMethodAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'amount', 'transaction_type', 'created_at']
    list_filter = ['transaction_type']
    search_fields = ['sender__username', 'recipient__username']

admin.site.register(Transaction, TransactionAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'read', 'created_at']
    list_filter = ['read']
    search_fields = ['user__username', 'message']

admin.site.register(Notification, NotificationAdmin)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['user', 'details', 'issued_on']
    search_fields = ['user__username']

admin.site.register(Invoice, InvoiceAdmin)




class KYCAdmin(admin.ModelAdmin):
    list_display = ['user', 'document_image_preview', 'verified']
    list_filter = ['verified']
    readonly_fields = ['document_image_preview']

    def document_image_preview(self, obj):
        if obj.document_image:
            return format_html('<img src="{}" style="width: 45px; height:45px;" />'.format(obj.document_image.url))
        return "No Image"

admin.site.register(KYC, KYCAdmin)

class BillPaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'bill_type', 'amount', 'paid_on']
    list_filter = ['bill_type']
    search_fields = ['user__username']

admin.site.register(BillPayment, BillPaymentAdmin)
