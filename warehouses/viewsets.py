from django.db.models import F
from warehouses.models import Warehouse, Inventory, Product
from rest_framework import viewsets
from warehouses.serializers import (
    WarehouseSerializer,
    InventorySerializer,
    ProductSerializer,
    DeleteProductSerializer,
)
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = (
        Inventory.objects.all().select_related("warehouse").prefetch_related("products")
    )
    serializer_class = InventorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().prefetch_related("inventory")
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            self.get_serializer(product).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        name = serializer.validated_data.get("name")
        inventory = serializer.validated_data.get("inventory")
        quantity = serializer.validated_data.get("quantity")
        product, created = Product.objects.update_or_create(
            name=name,
            inventory=inventory,
            defaults={"quantity": F("quantity") + quantity},
        )
        product.refresh_from_db()
        return product

    @swagger_auto_schema(
        request_body=DeleteProductSerializer,
        responses={200: "Quantity removed successfully", 400: "Quantity is not enough"},
    )
    def destroy(self, request, *args, **kwargs):
        request_data = request.data
        product_serializer = DeleteProductSerializer(data=request_data)
        product_serializer.is_valid(raise_exception=True)
        instance = self.get_object()
        if (
            instance.quantity > 0
            and instance.quantity - product_serializer.validated_data["quantity"] >= 0
        ):
            instance.quantity -= product_serializer.validated_data["quantity"]
            instance.save()
        else:
            return Response(
                {"message": "Quantity is not enough"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"detail": "Quantity removed successfully"}, status=status.HTTP_200_OK
        )
