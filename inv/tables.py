import django_tables2 as tables
from .models import InventoryItem

class InventoryItemTable(tables.Table):
    id = tables.Column(verbose_name="ID")

    actions = tables.TemplateColumn(
        template_name="inv/actions.html",
        verbose_name="",
        orderable=False,
        attrs={"th": {"class": "tight-col"}, "td": {"class": "tight-col"}}
    )

    class Meta:
        model = InventoryItem
        template_name = "django_tables2/bootstrap5.html"
        attrs = {"class": "table table-striped table-hover table-sm align-middle"}
        order_by = ("id",)
        sequence = (
            "id",
            "capex_opex",
            "type",
            "qty",
            "project",
            "assigned_bench",
            "cft_number",
            "pr_number",
            "po_number",
            "wo_number",
            "invoice_id",
            "description",
            "serial_number",
            "supplier",
            "status",
            "storage_location",
            "comments",
            "asset_number",
        )
        row_attrs = {
                    "id": lambda record: f"row-{record.pk}",
                }

