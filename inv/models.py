from django.db import models
from datetime import date, timedelta
from django.conf import settings
from django.utils import timezone

CERT_VALIDITY_DAYS = getattr(settings, "CERT_VALIDITY_DAYS", 365)
CERT_VALIDITY_MODE = getattr(settings, "CERT_VALIDITY_MODE", "rolling")

class CapexOpex(models.Model):
    code = models.CharField(max_length=20, unique=True)
    label = models.CharField(max_length=60, blank=True)
    def __str__(self):
        return self.label or self.code
    
class Project(models.Model):
    code = models.CharField(max_length=30, unique=True)
    label = models.CharField(max_length=100, blank=True)

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
    requires_certification = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Inventory item"
        verbose_name_plural = "Inventory items"
        ordering = ["id", "assigned_bench", "type", "supplier"]

    def __str__(self):
        return f"{self.type} - {self.description[:50]}".strip()

    def latest_certification(self):
        return self.certifications.order_by("-certification_date").first()

    @property
    def last_certification_date(self):
        c = self.latest_certification()
        return c.certification_date if c else None

    def expiration_date(self):
        c = self.latest_certification()
        if not c:
            return None
        if CERT_VALIDITY_MODE == "calendar_year":
            cd = c.certification_date
            return date(cd.year, 12, 31)
        return c.certification_date + timedelta(days=CERT_VALIDITY_DAYS)

    @property
    def days_remaining(self):
        exp = self.expiration_date()
        if not exp:
            return None
        today = timezone.localdate()
        return (exp - today).days

    @property
    def computed_status(self):
        if not self.requires_certification:
            return "not_applicable"
        if not self.last_certification_date:
            return "pending"
        exp = self.expiration_date()
        if exp and exp < timezone.localdate():
            return "expired"
        return "certified"

    def status_label(self):
        return {
            "not_applicable": "N/A",
            "pending": "Pending",
            "expired": "Expired",
            "certified": "Certified",
        }[self.computed_status]

def certification_upload_to(instance, filename):
    year = instance.certification_date.year if instance.certification_date else timezone.localdate().year
    return f"certifications/{instance.item_id}/{year}/{filename}"

class Certification(models.Model):
    item = models.ForeignKey(InventoryItem, related_name="certifications", on_delete=models.CASCADE)
    certification_date = models.DateField(default=timezone.localdate)
    file = models.FileField(upload_to=certification_upload_to)
    year = models.PositiveIntegerField(editable=False)

    class Meta:
        ordering = ["-certification_date"]
        indexes = [
            models.Index(fields=["item", "certification_date"]),
            models.Index(fields=["year"]),
        ]

    def save(self, *args, **kwargs):
        if not self.certification_date:
            self.certification_date = timezone.localdate()
        self.year = self.certification_date.year
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item} — {self.certification_date:%Y-%m-%d}"

class SavedFilter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inv_saved_filters")
    name = models.CharField(max_length=100)
    params = models.JSONField(default=dict)
    project_code = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("user", "name")

    def __str__(self):
        return f"{self.name} ({self.user})"