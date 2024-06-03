from django.db import IntegrityError
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

    def preform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            Product.objects.filter(
                name=serializer.validated_data["name"],
                inventory=serializer.validated_data["inventory"],
            ).update(quantity=F("quantity") + serializer.validated_data["quantity"])

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
            instance.quantity -= instance.quantity
            instance.save()
        else:
            return Response(
                {"message": "Quantity is not enough"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"detail": "Quantity removed successfully"}, status=status.HTTP_200_OK
        )
