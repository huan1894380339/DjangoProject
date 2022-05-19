from django.urls import path, include
from rest_framework import routers

from .views import ProductInstance, SignUp, UploadImage, CSVHandle, UploadImageView
from rest_framework import routers
app_name = 'app'

router = routers.DefaultRouter()
router.register(r'', ProductInstance, basename='product')
# router.register(r'upload-images/', UploadImage.as_view(), basename='images')
urlpatterns = [
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('upload-images/', UploadImage.as_view(), name = 'upload-images'),
    path('upload/', UploadImageView.as_view(), name = 'uploads-images'),
    # path('import-csv/', CSVHandleView.as_view(), name = 'import-csv'),
    path('import/', CSVHandle.as_view(), name = 'import'),
    path('product/', include(router.urls),)
]
urlpatterns = urlpatterns + router.urls
