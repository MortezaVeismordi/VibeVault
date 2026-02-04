from django.contrib import admin
from .models import Payment, PaymentLog, Refund


class PaymentLogInline(admin.TabularInline):
    model = PaymentLog
    extra = 0
    readonly_fields = ('created_at',)


class RefundInline(admin.TabularInline):
    model = Refund
    extra = 0


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('payment_method', 'status', 'created_at')
    search_fields = ('order__order_number', 'transaction_id')
    readonly_fields = ('transaction_id', 'created_at', 'updated_at', 'completed_at')
    inlines = [PaymentLogInline, RefundInline]


@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ('payment', 'status', 'message', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('payment__order__order_number', 'message')
    readonly_fields = ('created_at',)


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('payment', 'amount', 'reason', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('payment__order__order_number', 'reason')
