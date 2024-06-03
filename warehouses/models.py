import uuid
from model_utils.models import TimeStampedModel
from django.db import models


# We could improved the deleteion operation with making soft delete this would allow us to make indexes without costing much
class Warehouse(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    location = models.CharField(
        max_length=255
    )  # For a better implementation, we can use decimal langitutude and latitude or use postgresgis


class Inventory(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    warehouse = models.OneToOneField(
        Warehouse, on_delete=models.CASCADE, related_name="inventory"
    )


class Product(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="products"
    )
    description = models.TextField()
    quantity = models.PositiveBigIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "inventory"], name="unique_product_name_inventory"
            )
        ]
