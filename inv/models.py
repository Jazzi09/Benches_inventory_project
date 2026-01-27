
from django.db import models

class InventoryItem(models.Model):
    assigned_bench = models.CharField("Assigned Bench", max_length=100, blank=True)
    type = models.CharField("Type", max_length=100, blank=True)
    supplier = models.CharField("Supplier", max_length=100, blank=True)
    qty = models.DecimalField("QTY", max_digits=10, decimal_places=2, default=0)
    description = models.TextField("Description", blank=True)
    status = models.CharField("Status", max_length=50, blank=True)
    comments = models.TextField("Comments", blank=True)
    storage_location = models.CharField("Storage Location", max_length=100, blank=True)

    class Meta:
        verbose_name = "Inventory item"
        verbose_name_plural = "Inventory items"
        ordering = ["assigned_bench", "type", "supplier"]

    def __str__(self):
        return f"{self.type} - {self.description[:50]}".strip()
