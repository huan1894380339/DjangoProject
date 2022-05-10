from django.urls import URLPattern, path
from .views import *
app_name = 'app'
urlpatterns = [
    path('register',register_user,name="url_api")
]