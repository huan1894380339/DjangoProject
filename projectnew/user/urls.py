from django.urls import URLPattern, path
from .views import *
app_name = 'user'
urlpatterns = [
    path('register',register_user,name="url_api")
]