from __future__ import annotations

from django.contrib import admin

from .models import (
    Category, Contact, CustomerUser, Gallery, Order,
    Product, Supplier, CartItem, Membership, BlackListedToken, Discount,
)

from django.forms import ModelForm, PasswordInput

# Register your models here.
admin.site.register(Contact)
admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Discount)
admin.site.register(BlackListedToken)


class UserForm(ModelForm):
    class Meta:
        widgets = {
            'password':PasswordInput(render_value = True)
        }


class EventPhotosInline(admin.StackedInline):
    model = Gallery


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [EventPhotosInline]
    list_filter = ('active', 'category')
    list_display = ('id', 'title', 'price', 'category', 'active')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'status')
    list_filter = ['status']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('id', 'status', 'user', 'updated_at', 'show_cartitem')
    list_filter = ['status']

    def show_cartitem(self, obj):
        return '\n'.join([str(a.id) for a in obj.cart_item.all()])
    show_cartitem.short_description = 'Cart Item (id)'


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'voucher')


@admin.register(CustomerUser,)
class CustomerUserAdmin(admin.ModelAdmin):
    form = UserForm
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (
            ('Personal info'), {
                'classes': ('collapse',),
                'fields': ('phone_number', 'address', 'first_name', 'last_name'),
            },
        ),
        (
            ('Permissions'), {
                'classes': ('collapse',),
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            },
        ),
        (
            ('Important dates'), {
                'classes': ('collapse',),
                'fields': ('last_login', 'date_joined'),
            },
        ),
    )
    list_display = ('id', 'username', 'email', 'is_active')


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product')
