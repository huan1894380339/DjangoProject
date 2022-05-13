from atexit import register
from django.contrib import admin
from .models import CustomerUser, Contact, Product, Cart, Order, Supplier, Category,Gallery
# Register your models here.
admin.site.register(CustomerUser)
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Gallery)

