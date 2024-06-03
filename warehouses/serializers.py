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
    products = serializers.ManyRelatedField(
        child_relation=serializers.PrimaryKeyRelatedField(
            queryset=Product.objects.all().prefetch_related("inventory")
        ),
        required=False,
    )

    class Meta:
        model = Inventory
        fields = ["id", "warehouse", "products"]
        read_only_fields = [
            "id",
        ]


class DeleteProductSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, required=True)


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[])
    inventory = serializers.PrimaryKeyRelatedField(
        queryset=Inventory.objects.all().prefetch_related("products"), validators=[]
    )

    class Meta:
        model = Product
        fields = ["id", "name", "inventory", "quantity"]
        depth = 1
        read_only_fields = [
            "id",
        ]

    def get_validators(self):
        """
        Overriding method to disable a specific unique_together validator.
        """
        validators = super(ProductSerializer, self).get_validators()
        for validator in validators:
            if hasattr(validator, "fields") and set(validator.fields) == {
                "name",
                "inventory",
            }:
                validators.remove(validator)
                break
        return validators
