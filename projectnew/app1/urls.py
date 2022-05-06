from djagon.urls import path
from .vews import *
app_name = 'app1'
urlpatterns = [
    path('app1',api1,name="url_api1")
]