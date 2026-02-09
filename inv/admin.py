
from django.contrib import admin
from .models import InventoryItem, AssignedBench, ItemType, Supplier, Status, StorageLocation, CapexOpex, Project

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = (
        "capex_opex",
        "project",
        "assigned_bench",
        "type", 
        "qty",
        "cft_number",
        "pr_number",
        "po_number",
        "wo_number",
        "invoice_id",
        "description",
        "serial_number",
        "supplier",
        "status",
        "comments",
        "storage_location",
        "asset_number",
)
    
    list_filter = ("assigned_bench", "type", "status", "storage_location", "supplier")

    search_fields = (
        "description",
        "comments",
        "supplier__code", "supplier__label",
        "type__code", "type__label",
        "assigned_bench__code", "assigned_bench__label",
        "storage_location__code", "storage_location__label",
        "status__code", "status__label",
    )


@admin.register(AssignedBench)

class AssignedBenchAdmin(admin.ModelAdmin):
    list_display = ("code", "label")
    search_fields = ("code", "label")
    ordering = ("code",)

@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "label")
    search_fields = ("code", "label")
    ordering = ("code",)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("code", "label")
    search_fields = ("code", "label")
    ordering = ("code",)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("code", "label")
    search_fields = ("code", "label")
    ordering = ("code",)

@admin.register(StorageLocation)
class StorageLocationAdmin(admin.ModelAdmin):
    list_display = ("code", "label")
    search_fields = ("code", "label")
    ordering = ("code",)


@admin.register(CapexOpex)
class CapexOpexAdmin(admin.ModelAdmin):
    list_display = ("code", "label")
    search_fields = ("code", "label")
    ordering = ("code",)

@admin.register(Project)
class Project(admin.ModelAdmin):
    list_display = ("code", "label")
    search_fields = ("code", "label")
    ordering = ("code",)
