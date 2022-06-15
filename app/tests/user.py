import email
import factory
from faker import Faker
from app.models import CustomerUser


facker = Faker()
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomerUser
