from turtle import title
from unicodedata import category
import factory
from faker import Faker
from app.models import Category

facker = Faker()
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    title = facker.text(max_nb_chars=20)
    slug = facker.text(max_nb_chars=20)
    description = facker.text(max_nb_chars=100)
    active = True