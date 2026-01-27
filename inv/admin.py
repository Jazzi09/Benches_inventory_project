
from django.contrib import admin
from .models import InventoryItem

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("assigned_bench", "type", "supplier", "qty", "status", "storage_location")
    list_filter = ("assigned_bench", "type", "status", "storage_location", "supplier")
    search_fields = ("description", "comments", "supplier", "type", "assigned_bench", "storage_location")
