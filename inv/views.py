
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import InventoryItem
from .forms import InventoryItemForm


def inventory_list(request):
    q = request.GET.get("q", "")
    qs = InventoryItem.objects.all()
    if q:
        qs = qs.filter(description__icontains=q)
    return render(request, "inv/list.html", {"items": qs, "q": q})


def inventory_create(request):
    if request.method == "POST":
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inv:list")
    else:
        form = InventoryItemForm()
    return render(request, "inv/create.html", {"form": form})
