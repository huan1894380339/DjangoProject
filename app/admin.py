from __future__ import annotations

from django.contrib import admin

from .models import (
    Category, Contact, CustomerUser, Gallery, Order,
    Product, Supplier, CartItem, Membership,
)

# Register your models here.
admin.site.register(CustomerUser)
admin.site.register(Contact)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Gallery)
admin.site.register(Membership)


class EventPhotosInline(admin.StackedInline):
    model = Gallery


@admin.register(Product)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventPhotosInline]
