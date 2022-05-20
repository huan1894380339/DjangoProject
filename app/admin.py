from django.contrib import admin

from .models import (
    Cart,
    Category,
    Contact,
    CustomerUser,
    Gallery,
    Order,
    Product,
    Supplier,
)

# Register your models here.
admin.site.register(CustomerUser)
admin.site.register(Contact)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Gallery)


class EventPhotosInline(admin.StackedInline):
    model = Gallery


@admin.register(Product)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventPhotosInline]
