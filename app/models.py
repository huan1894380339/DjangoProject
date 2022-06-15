from __future__ import annotations
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
from gdstorage.storage import GoogleDriveStorage
from app.constant import ITEM_STATUS
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

# Create your models here.
date_field = models.DateField(default=timezone.now)


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
    voucher = models.FloatField()

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
        return '%s id:%s' % (self.title, str(self.id))

    @property
    def img_url(self):
        if self.img_product:
            return self.img_product.url
        return None


class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    day_start = models.DateTimeField()
    day_end = models.DateTimeField()
    value_discount = models.IntegerField()


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


class Order(models.Model):
    user = models.ForeignKey(
        CustomerUser, on_delete=models.CASCADE, related_name='order_user',
    )
    shiping_address = models.CharField(blank=False, null=False, max_length=255)
    order_decription = models.TextField(blank=False, null=False)
    # subtotal =models.FloatField(default=0)
    phone = models.CharField(null=True, max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=ITEM_STATUS, max_length=2, default='NE')

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
        membership = Membership.objects.select_related('customeruser').filter(
            customeruser=self.user.id,
        ).first()
        total = self.quantity * self.product.price * \
            ((100 - membership.voucher) / 100)
        return total


class BlackListedToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.ForeignKey(
        CustomerUser, related_name='token_user', on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('token', 'user')


@receiver(post_save, sender=Order, dispatch_uid='update_voucher')
def update_voucher(sender, instance, **kwargs):
    membership = Membership.objects.get(customeruser=instance.user.id)
    all_order = Order.objects.filter(user=instance.user, status='SE')
    voucher = (sum(order.cart_total for order in all_order) * 1e-8) * 100
    membership.voucher = voucher
    membership.save()
