from django.db.models.signals import post_save
from django.dispatch import receiver
from warehouses.models import Warehouse, Inventory


@receiver(post_save, sender=Warehouse)
def create_inventory_for_warehouse(sender, instance, created, **kwargs):
    if created:
        Inventory.objects.create(warehouse=instance)
