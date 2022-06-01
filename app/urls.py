from __future__ import annotations

from django.urls import include, path
from rest_framework import routers
from app.views.product import ProductViewSet
from app.views.order import OrderViewSet
from app.views.cartritem import CartItemViewset
from app.views.user import UserViewSet
from app.utils import active
app_name = 'app'

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)

router.register(r'order', OrderViewSet)
router.register(
    r'cartitem/manage-cartitem',
    CartItemViewset, basename='cartitem',
)
router.register(r'user', UserViewSet, basename='user')
urlpatterns = [
    path('user/active/<uidb64>/<token>/', active, name='active'),
    path('', include(router.urls)),
]
urlpatterns = urlpatterns + router.urls
