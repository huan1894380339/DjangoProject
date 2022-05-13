from atexit import register
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import CustomerUser, Contact, Product, Cart, Order, Supplier, Category,Gallery
# Register your models here.
admin.site.register(CustomerUser)
admin.site.register(Contact)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Gallery)

# @admin.register(Product)
# class ProductAdmin(ImportExportModelAdmin):
#     pass

class EventPhotosInline(admin.StackedInline):
    model = Gallery
@admin.register(Product)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventPhotosInline,]