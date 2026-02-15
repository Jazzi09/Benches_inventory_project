import django_filters
from .models import InventoryItem, AssignedBench, ItemType, Supplier, Status, StorageLocation

class InventoryItemFilter(django_filters.FilterSet):
    assigned_bench = django_filters.ModelChoiceFilter(
        field_name="assigned_bench",
        queryset=AssignedBench.objects.all(),
        empty_label="All",
        label="Assigned bench"
    )
    type = django_filters.ModelChoiceFilter(
        field_name="type",
        queryset=ItemType.objects.all(),
        empty_label="All",
        label="Type"
    )
    supplier = django_filters.ModelChoiceFilter(
        field_name="supplier",
        queryset=Supplier.objects.all(),
        empty_label="All",
        label="Supplier"
    )
    status = django_filters.ModelChoiceFilter(
        field_name="status",
        queryset=Status.objects.all(),
        empty_label="All",
        label="Status"
    )
    storage_location = django_filters.ModelChoiceFilter(
        field_name="storage_location",
        queryset=StorageLocation.objects.all(),
        empty_label="All",
        label="Storage location"
    )

    class Meta:
        model = InventoryItem
        fields = [
            "type",
            "assigned_bench",
            "supplier",
            "status",
            "storage_location",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.form.fields.items():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css + " form-control form-control-sm").strip()
