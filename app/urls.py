from django.urls import include, path
from rest_framework import routers

from app.views.product import (
    ImportProductFromCSV,
    ProductInstance,
    UploadImageProductFromPath,
)

app_name = "app"

router = routers.DefaultRouter()
router.register(r"", ProductInstance, basename="product")
urlpatterns = [
    # path('sign-up/', SignUp.as_view(), name='sign-up'),
    path("upload-images/", UploadImageProductFromPath.as_view(), name="uploads-images"),
    path("import-product-from-csv/", ImportProductFromCSV.as_view(), name="import"),
    path("product/", include(router.urls)),
]
urlpatterns = urlpatterns + router.urls
