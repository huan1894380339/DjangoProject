import factory
from faker import Faker
from app.models import Product


facker = Faker()


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    code = facker.ean(length=8)
    category = facker.word()
    title = facker.text(max_nb_chars=20)
    img_product = facker.file_name(category='image')
    description = ''
    price = facker.random_int(min=1000, max=2000)
    active = True
