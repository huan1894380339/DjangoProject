from __future__ import annotations

from django.urls import include, path
from rest_framework import routers
from app.views.product import ProductViewSet
from app.views.order import OrderViewSet
from app.views.cartritem import CartItemViewset
from app.views.user import UserViewSet
from app.views.report import ReportViewSet
from app.utils import active, reset_password
app_name = 'app'

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)

router.register(r'order', OrderViewSet)
router.register(
    r'cartitem/manage-cartitem',
    CartItemViewset, basename='cartitem',
)
router.register(r'user', UserViewSet, basename='user')
router.register(r'report', ReportViewSet, basename='report')
urlpatterns = [
    path('user/active/<uidb64>/<token>/', active, name='active'),
    path('user/reset_password/<uidb64>/<token>/', reset_password, name='reset'),
    path('', include(router.urls)),
]
urlpatterns = urlpatterns + router.urls
