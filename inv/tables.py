import django_tables2 as tables
from .models import InventoryItem
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

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



class UsersTable(tables.Table):
    id = tables.Column(verbose_name="ID")

    actions = tables.TemplateColumn(
        template_name="inv/user_actions.html",
        extra_context={"group_name": "Admin"},
        verbose_name="",
        orderable=False,
        attrs= {
        "th": {"class": "text-center"},  # center header
        "td": {"class": "text-center"},  # center cell contents
        },
    )

    class Meta:
        model = User
        template_name = "django_tables2/bootstrap5.html"
        fields = ('id', "username", "email", "date_joined")
        attrs = {"class": "table table-striped table-hover table-sm align-middle"}
        order_by = ("id",)
