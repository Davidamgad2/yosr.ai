from rest_framework.routers import DefaultRouter
from django.urls import path, include
from warehouses.viewsets import WarehouseViewSet, InventoryViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"warehouses", WarehouseViewSet)
router.register(r"inventories", InventoryViewSet)
router.register(r"products", ProductViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
