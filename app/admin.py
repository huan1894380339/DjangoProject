from __future__ import annotations

from django.contrib import admin

from .models import Cart
from .models import Category
from .models import Contact
from .models import CustomerUser
from .models import Gallery
from .models import Order
from .models import Product
from .models import Supplier

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
