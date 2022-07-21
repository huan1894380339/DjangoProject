from __future__ import annotations
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
from gdstorage.storage import GoogleDriveStorage
from numpy import product
from app.constant import ITEM_STATUS_ORDER, ITEM_STATUS_CART
from django.core.validators import MinValueValidator, MaxValueValidator
# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

# Create your models here.
date_field = models.DateField(default=timezone.now)


class CustomerUser(AbstractUser):
    email = models.EmailField()
    phone_number = models.CharField(default='', max_length=10, blank=True)
    address = models.CharField(default='', max_length=255, blank=True)
    # code_verify = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.username


class Membership(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    rank = models.IntegerField(default=1)
    voucher = models.FloatField(default=0)

    @property
    def get_voucher(self):
        all_order = self.order_user.all()
        voucher = sum(order.cart_total for order in all_order) * 0.01
        return voucher


class Contact(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    mail = models.EmailField(max_length=254, blank=False, null=False)
    content = models.CharField(max_length=1000, blank=False, null=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mail


class Category(models.Model):
    title = models.CharField(blank=False, null=False, max_length=200)
    slug = models.CharField(blank=False, null=False, max_length=100)
    description = models.TextField(blank=False, null=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    code = models.CharField(max_length=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(
        blank=False, null=False,
        max_length=200, unique=True,
    )
    img_product = models.FileField(
        upload_to='maps/', storage=gd_storage, blank=True,
    )
    description = models.TextField(blank=False, null=False)
    price = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(2000)],
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def img_url(self):
        if self.img_product:
            return self.img_product.url
        return None


class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    day_start = models.DateTimeField()
    day_end = models.DateTimeField()
    value_discount = models.FloatField()


class Gallery(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='prod_gallery',
    )
    img_product = models.FileField(
        upload_to='maps/', storage=gd_storage, blank=True,
    )


class Supplier(models.Model):
    name_supplier = models.CharField(blank=False, null=False, max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    sale_price = models.IntegerField(default=0)
    inventory = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'id:{self.id} - {self.product}'


class CartItem(models.Model):
    user = models.ForeignKey(
        CustomerUser, on_delete=models.CASCADE, limit_choices_to={
            'user_cart__isnull': False,
        }, related_name='user_cart',
    )
    status = models.CharField(
        choices=ITEM_STATUS_CART,
        max_length=1, default='W',
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='cartitem_product',
    )
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

# TODO: Calculate price total for items, handle discount
    @property
    def item_total(self):
        try:
            discount = Discount.objects.get(product=self.product)
            if timezone.now() < discount.day_end:
                price_discount = self.product.price - \
                    self.product.price * discount.value_discount
                total = self.quantity * price_discount
            else:
                total = self.quantity * self.product.price
        except Exception:
            total = self.quantity * self.product.price
        return total

    # TODO: Calculate price total after apply voucher for items 
    def item_total_after_apply_voucher(self):
        membership = Membership.objects.select_related('user').filter(
            user=self.user.id,
        ).first()
        total = self.item_total - self.item_total* membership.voucher
        return round(total, 1)

# TODO: Limit choices for field model
# FIXME: anh hau fix    


class Order(models.Model):
    user = models.ForeignKey(
        CustomerUser, on_delete=models.CASCADE, related_name='order_user', limit_choices_to={
            'user_cart__isnull': False,
        },
    )
    cart_item = models.ManyToManyField(CartItem, related_name='order_cartitem')
    shiping_address = models.CharField(blank=False, null=False, max_length=255)
    order_decription = models.TextField(blank=False, null=False)
    phone = models.CharField(null=True, max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        choices=ITEM_STATUS_ORDER, max_length=2, default='NE',
    )

    def __str__(self):
        return str(self.id)

    @property
    def cart_total(self):
        cartitem = self.cart_item.all()
        total = sum(
            product.item_total_after_apply_voucher()
            for product in cartitem
        )
        return round(total, 1)


class BlackListedToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.ForeignKey(
        CustomerUser, related_name='token_user', on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('token', 'user')
