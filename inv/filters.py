import django_filters
from .models import InventoryItem

class InventoryItemFilter(django_filters.FilterSet):
    assigned_bench = django_filters.ChoiceFilter(
        field_name="assigned_bench",
        choices=InventoryItem.ASSIGNED_CHOICES,
        empty_label="All",
        label="Assigned bench"
    )
    type = django_filters.ChoiceFilter(
        field_name="type",
        choices=InventoryItem.TYPE_CHOICES,
        empty_label="All",
        label="Type"
    )
    supplier = django_filters.ChoiceFilter(
        field_name="supplier",
        choices=InventoryItem.SUPPLIER_CHOICES,
        empty_label="All",
        label="Supplier"
    )
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=InventoryItem.STATUS_CHOICES,
        empty_label="All",
        label="Status"
    )

class Meta:
    model = InventoryItem
    fields = ["assigned_bench", "type", "supplier", "status"]


def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for _, field in self.form.fields.items():
        css = field.widget.attrs.get("class", "")
        field.widget.attrs["class"] = (css + " form-control form-control-sm").strip()
