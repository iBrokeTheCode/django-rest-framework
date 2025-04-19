from django.contrib import admin

from api.models import Order, OrderItem, User


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)


admin.site.register(User)
