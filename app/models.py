from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models
from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

# Create your models here.


class CustomerUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(default='', max_length=10)
    address = models.CharField(default='', max_length=255)
    # code_verify = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.username


class Membership(models.Model):
    customeruser = models.ForeignKey(CustomerUser, on_delete=models.Model)
    rank = models.IntegerField()
    voucher = models.IntegerField()

    @property
    def get_voucher(self):
        all_order = self.order_user.all()
        voucher = sum(order.cart_total for order in all_order) * 1e-8
        return voucher


class Contact(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    mail = models.EmailField(max_length=254, blank=False, null=False)
    content = models.CharField(max_length=1000, blank=False, null=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mail


class Category(models.Model):
    title = models.CharField(default='', max_length=200)
    slug = models.CharField(default='', max_length=100)
    description = models.TextField(default='')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    code = models.CharField(max_length=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(default='', max_length=200)
    img_product = models.FileField(
        upload_to='maps/', storage=gd_storage, blank=True,
    )
    description = models.TextField(default='')
    price = models.FloatField(default=0)
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
    day_end = models.DateField()


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
    name_supplier = models.CharField(default='', max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    sale_price = models.IntegerField(default=0)
    inventory = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'id:{self.id} - {self.product}'


class Order(models.Model):
    user = models.ForeignKey(
        CustomerUser, on_delete=models.CASCADE, related_name='order_user',
    )
    shiping_address = models.CharField(default='', max_length=255)
    order_decription = models.TextField(default='')
    # subtotal =models.FloatField(default=0)
    phone = models.CharField(null=True, max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    @property
    def cart_total(self):
        cartitem = self.orderitem.all()
        total = sum(
            product.item_total_after_apply_voucher()
            for product in cartitem
        )
        return total


class CartItem(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='orderitem',
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='cartitem_product',
    )
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def item_total(self):
        total = self.quantity * self.product.price
        return total

    def item_total_after_apply_voucher(self):
        membership = Membership.objects.get(id=self.user.id)
        total = self.quantity * self.product.price * \
            ((100 - membership.voucher) / 100)
        return total
