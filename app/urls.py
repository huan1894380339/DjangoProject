from email.mime import base
from django.urls import path, include
from rest_framework import routers

from projectnew import urls
from .views import ProductInstance,SignUp
from rest_framework import routers
app_name = 'app'

router = routers.DefaultRouter()
router.register(r'', ProductInstance, basename='product')
urlpatterns = [
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('product/', include(router.urls),)
]
