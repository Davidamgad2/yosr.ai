from warehouses.models import Warehouse, Inventory, Product
from rest_framework import serializers


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["id", "name", "location"]
        read_only_fields = [
            "id",
        ]


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["warehouse"]
        read_only_fields = [
            "id",
        ]


class DeleteProductSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, required=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "inventory", "quantity"]
        depth = 1
        read_only_fields = [
            "id",
        ]
