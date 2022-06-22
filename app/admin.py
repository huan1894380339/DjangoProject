from __future__ import annotations

from django.contrib import admin

from .models import (
    Category, Contact, CustomerUser, Gallery, Order,
    Product, Supplier, CartItem, Membership, BlackListedToken, Discount,
)


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


# Register your models here.
admin.site.register(CustomerUser)
admin.site.register(Contact)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Gallery)
admin.site.register(Membership)
admin.site.register(Discount)
admin.site.register(BlackListedToken)


class EventPhotosInline(admin.StackedInline):
    model = Gallery


@admin.register(Product)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventPhotosInline]
