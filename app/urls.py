from __future__ import annotations
from app.views.user import SignUp, SignIn, VerifyAcount

from django.urls import include, path
from rest_framework import routers
from app.views.product import (
    ImportProductFromCSV, ProductInstance,
    UploadImageProductFromPath, GetListProductByCategory, GetProductNew, GetListnewProductByCategory,
)
from app.views.order import ManageOrder, GetAllOrderByUser
from app.views.cartritem import CartItemViewset
from app.views.user import SignOut, ChangePassword
from app.utils import active
app_name = 'app'

router = routers.DefaultRouter()
router.register(r'product/manage-product', ProductInstance)
router.register(r'order/manage-order', ManageOrder)
router.register(
    r'cartitem/manage-cartitem',
    CartItemViewset, basename='cartitem',
)
urlpatterns = [
    path('user/sign-up/', SignUp.as_view(), name='sign-up'),
    path('user/sign-in/', SignIn.as_view(), name='sign-in'),
    path(
        'product/upload-images', UploadImageProductFromPath.as_view(),
        name='uploads-images',
    ),
    path(
        'product/import-product-from-csv/',
        ImportProductFromCSV.as_view(), name='import',
    ),
    path(
        'product/get-product-by-category',
        GetListProductByCategory.as_view(), name='Get product by Category',
    ),
    path(
        'product/get-product-new',
        GetProductNew.as_view(), name='Get product New',
    ),
    path(
        'product/get-product-new-by-category',
        GetListnewProductByCategory.as_view(), name='Get List newProduct by Category',
    ),
    path(
        'order/get-all-oder-by-user',
        GetAllOrderByUser.as_view(), name='Get all order by user',
    ),
    path(
        'user/verify-acount', VerifyAcount.as_view(),
        name='Verify acount by code',
    ),
    path(
        'user/sign-out', SignOut.as_view(),
        name='Sign Out',
    ),
    path(
        'user/change-password', ChangePassword.as_view(),
        name='Change Password',
    ),
    path('user/active/<uidb64>/<token>/', active, name='active'),
    path('', include(router.urls)),
]
urlpatterns = urlpatterns + router.urls
