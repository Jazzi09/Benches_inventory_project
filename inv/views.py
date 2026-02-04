
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
import math

from django_tables2 import SingleTableView
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView

from .models import InventoryItem
from .forms import InventoryItemForm
from .tables import InventoryItemTable
from .filters import InventoryItemFilter

class InventoryListView(SingleTableMixin, FilterView):
    model = InventoryItem
    table_class = InventoryItemTable
    template_name = "inv/list_tables2.html"
    filterset_class = InventoryItemFilter
    table_pagination = {
        "per_page": 10         
    }

    def get_table_pagination(self, table):
        try:
            per_page = int(self.request.GET.get("per_page", 10))
        except ValueError:
            per_page = 10
        if per_page not in (10, 25, 50, 75, 100):
            per_page = 10
        return {"per_page": per_page}

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(description__icontains=q)
        return qs

def inventory_create(request):
    if request.method == "POST":
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            obj = form.save()
            per_page = 10
            total = InventoryItem.objects.count()
            last_page = math.ceil(total / per_page)
            return redirect(reverse("inv:list") + f"?page={last_page}#row-{obj.pk}")
    else:
        form = InventoryItemForm()
    return render(request, "inv/create.html", {"form": form, "mode": "create"})


def inventory_edit(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == "POST":
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item actualizado")
            return redirect("inv:list")
    else:
        form = InventoryItemForm(instance=item)
    return render(request, "inv/edit.html", {"form": form, "item": item})

@require_POST
def inventory_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    item.delete()
    return redirect('inv:list')
