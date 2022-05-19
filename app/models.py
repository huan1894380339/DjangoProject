from django.db import models
from django.contrib.auth.models import AbstractUser
from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

# Create your models here.
class CustomerUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(default='', max_length=10)
    address = models.CharField(default='', max_length=255)
    
    def __str__(self) -> str:
        return self.username



class Membership(models.Model):
    customeruser = models.ForeignKey(CustomerUser, on_delete=models.Model)
    rank = models.IntegerField()
    voucher = models.IntegerField()

class Contact(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    mail = models.EmailField(max_length=254,blank=False, null=False)
    content = models.CharField(max_length=1000, blank=False, null=False)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.mail


class Category(models.Model):
    title = models.CharField(default='', max_length=200)
    slug = models.CharField(default='',max_length=100)
    description = models.TextField(default='')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    code = models.CharField( max_length=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(default='', max_length=200)
    img_product = models.FileField(upload_to='maps/', storage=gd_storage, blank=True)
    description = models.TextField(default='')
    price = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    def __str__(self):
        return str(self.id)

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prod_gallery")
    img_product = models.FileField(upload_to='maps/', storage=gd_storage, blank=True)
    # def upload(request):
    #     if request.method == "POST":
    #         images = request.FILES.getlist('images')
    #         for image in images:
    #             Gallery.objects.create(images=image)
    #     images = Gallery.objects.all()


class Supplier(models.Model):
    name_supplier = models.CharField(default='', max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    sale_price = models.IntegerField(default=0)
    inventory = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'id:{self.id} - {self.product}'


class Cart(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def get_cart_total(self):
        cartitem =  self.cartitem_set.all()
        total = sum([product.get_total for product in cartitem])
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f'cart_id:{self.cart}'
        
    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total

class Order(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    shiping_address = models.CharField(default='', max_length=255)
    order_decription = models.TextField(default='')
    # subtotal =models.FloatField(default=0)
    phone = models.CharField(null= True, max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
