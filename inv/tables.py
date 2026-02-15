import django_tables2 as tables
from .models import InventoryItem
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html


class InventoryItemTable(tables.Table):
    id = tables.Column(verbose_name="ID")

    actions = tables.TemplateColumn(
        template_name="inv/actions.html",
        verbose_name="",
        orderable=False,
        attrs={"th": {"class": "tight-col"}, "td": {"class": "tight-col"}}
    )
    
    required_certification = tables.Column(
        verbose_name="Required certification",
        empty_values=(),
        attrs={
                "td": {"class": "col-required-cert"},
                "th": {"class": "col-required-cert"},
            },
        )
    
    description = tables.Column(
        verbose_name="Description",
        attrs={
                "td": {"class": "col-desc"},
                "th": {"class": "col-desc"},
            },
        )
    
    def render_description(self, value):
        return format_html(
            '<div class="desc-cell" title="{}">{}</div>',
            value,
            value,
        )

    class Meta:
        model = InventoryItem
        template_name = "django_tables2/bootstrap5.html"
        attrs = {"class": "table table-striped table-hover table-sm align-middle"}
        fields = (
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
            "required_certification", 
        )

        row_attrs = {
                    "id": lambda record: f"row-{record.pk}",
                }
    
    def render_required_certification(self, record: InventoryItem):
        status = record.computed_status
        badge_class = {
            "certified": "bg-success",
            "pending": "bg-warning text-dark",
            "expired": "bg-danger",
            "not_applicable": "bg-secondary",
        }.get(status, "bg-secondary")

        label = {
            "certified": "Certified",
            "pending": "Pending",
            "expired": "Expired",
            "not_applicable": "N/A",
        }.get(status, "N/A")

        history_url = reverse("inv:certification_history", kwargs={"pk": record.pk})

        days_part = ""
        if record.days_remaining is not None and status != "not_applicable":
            days_part = format_html('<small class="text-muted ms-2">({} days)</small>', record.days_remaining)

        if status == "not_applicable":
            return format_html('<span class="badge {}">{}</span>{}', badge_class, label, days_part)

        return format_html(
            '<span class="badge {}">{}</span>{} '
            '<a class="btn btn-outline-primary btn-sm ms-2" href="{}">View history</a>',
            badge_class, label, days_part, history_url
        )

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
