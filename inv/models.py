
from django.db import models

class InventoryItem(models.Model):
    
    ASSIGNED_L21 = "L21"
    ASSIGNED_L22 = "L22"
    ASSIGNED_LO1 = "LO1"

    ASSIGNED_CHOICES = [
        (ASSIGNED_L21, "CADMsL2+_1"),
        (ASSIGNED_L22, "CADMsL2+_2"),
        (ASSIGNED_LO1, "CADMSLo_1"),
    ]

    TYPE_BENCH = "BENCH"
    TYPE_LICENSE = "LICENSE"
    TYPE_HARNESS = "HARNESS"
    TYPE_RADAR = "RADAR"
    TYPE_CAMERA = "CAMERA"
    TYPE_ECU = "ECU"
    TYPE_OTHER = "OTHER"

    TYPE_CHOICES = [
        (TYPE_BENCH, "Bench equipment"),
        (TYPE_LICENSE, "License"),
        (TYPE_HARNESS, "Harness"),
        (TYPE_RADAR, "Radar"),
        (TYPE_CAMERA, "Camera"),
        (TYPE_ECU, "ECU"),
        (TYPE_OTHER, "Other"),
    ]
    
    STATUS_WORKING = "WORKING"
    STATUS_LEND = "LEND"
    STATUS_DAMAGED = "DAMAGE"

    STATUS_CHOICES = [
        (STATUS_WORKING, "Working"),
        (STATUS_LEND, "Lend"),
        (STATUS_DAMAGED, "Damaged"),
    ]

    SUPPLIER_APTIV = "APTIV"
    SUPPLIER_VECTOR = "VECTOR"
    SUPPLIER_LAUTERBACH = "LAUTERBACH"
    SUPPLIER_DELL = "DELL"
    SUPPLIER_VALLEY = "VALLEY_INT"

    SUPPLIER_CHOICES = [
        (SUPPLIER_APTIV, "Aptiv"),
        (SUPPLIER_VECTOR, "Vector"),
        (SUPPLIER_LAUTERBACH, "Lauterbach"),
        (SUPPLIER_DELL, "Dell"),
        (SUPPLIER_VALLEY, "Valley Int"),
    ]
    
    STORAGE_BENCH = "BENCH"
    STORAGE_GABINET = "GABINET"
    STORAGE_NA = "NA"

    STORAGE_CHOICES = [
        (STORAGE_BENCH, "Bench Desk"),
        (STORAGE_GABINET, "Gabinet 1"),
        (STORAGE_NA, "N/A"),
    ]

    assigned_bench = models.CharField("Assigned Bench", max_length=30, choices=ASSIGNED_CHOICES)
    type = models.CharField("Type", max_length=20, choices=TYPE_CHOICES)
    supplier = models.CharField("Supplier", max_length=30, choices=SUPPLIER_CHOICES)
    qty = models.PositiveIntegerField("QTY", default=0)
    description = models.TextField("Description", blank=True)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES)
    comments = models.TextField("Comments", blank=True)
    storage_location = models.CharField("Storage Location", max_length=20, choices=STORAGE_CHOICES)

    class Meta:
        verbose_name = "Inventory item"
        verbose_name_plural = "Inventory items"
        ordering = ["id", "assigned_bench", "type", "supplier"]

    def __str__(self):
        return f"{self.type} - {self.description[:50]}".strip()
