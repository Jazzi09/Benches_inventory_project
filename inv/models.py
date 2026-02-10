
from django.db import models
from django.utils.text import slugify


class CapexOpex(models.Model):
    code = models.CharField(max_length=20, unique=True)
    label = models.CharField(max_length=60, blank=True)
    def __str__(self):
        return self.label or self.code
    
class Project(models.Model):
    code = models.CharField(max_length=30, unique=True)
    label = models.CharField(max_length=100, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            base = self.label or self.code
            self.slug = slugify(base)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.label or self.code

class AssignedBench(models.Model):
    code = models.CharField(max_length=30, unique=True)
    label = models.CharField(max_length=60, blank=True)
    def __str__(self):
        return self.label or self.code

class ItemType(models.Model):
    code = models.CharField(max_length=20, unique=True)
    label = models.CharField(max_length=60, blank=True)
    def __str__(self):
        return self.label or self.code

class Supplier(models.Model):
    code = models.CharField(max_length=30, unique=True)
    label = models.CharField(max_length=60, blank=True)
    def __str__(self):
        return self.label or self.code

class Status(models.Model):
    code = models.CharField(max_length=20, unique=True)
    label = models.CharField(max_length=60, blank=True)
    def __str__(self):
        return self.label or self.code

class StorageLocation(models.Model):
    code = models.CharField(max_length=20, unique=True)
    label = models.CharField(max_length=60, blank=True)
    def __str__(self):
        return self.label or self.code


class InventoryItem(models.Model):
    capex_opex = models.ForeignKey(CapexOpex, on_delete=models.PROTECT, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, null=True, blank=True)
    assigned_bench = models.ForeignKey(AssignedBench, on_delete=models.PROTECT, null=True, blank=True)
    type = models.ForeignKey(ItemType, on_delete=models.PROTECT, null=True, blank=True)
    qty = models.PositiveIntegerField("QTY", default=0)
    cft_number = models.CharField("CFT #", max_length=100, blank=True, default="")
    pr_number = models.CharField("PR #", max_length=100, blank=True, default="")
    po_number = models.CharField("PO #", max_length=100, blank=True, default="")
    wo_number = models.CharField("WO", max_length=100, blank=True, default="")
    invoice_id = models.CharField("Invoice ID", max_length=100, blank=True, default="")
    description = models.TextField("Description", blank=True) 
    serial_number = models.CharField("Serial #", max_length=200, blank=True, default="")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True, blank=True)
    comments = models.TextField("Comments", blank=True)
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.PROTECT, null=True, blank=True)
    asset_number = models.CharField("Asset #", max_length=200, blank=True, default="")

    class Meta:
        verbose_name = "Inventory item"
        verbose_name_plural = "Inventory items"
        ordering = ["id", "assigned_bench", "type", "supplier"]

    def __str__(self):
        return f"{self.type} - {self.description[:50]}".strip()
