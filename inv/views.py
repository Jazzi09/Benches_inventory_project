
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponse
import math

from django_tables2 import SingleTableView
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django_tables2 import RequestConfig

from .models import InventoryItem, Project
from .forms import InventoryItemForm, UsrCreation
from .tables import InventoryItemTable
from .filters import InventoryItemFilter


@login_required
@permission_required("inv.view_inv")
def inventory_by_project(request, project_code):
    current_project = get_object_or_404(Project, code=project_code)
    qs = (InventoryItem.objects
          .filter(project=current_project)
          .select_related('type', 'supplier', 'status', 'assigned_bench')
          .order_by('id'))
    f = InventoryItemFilter(request.GET, queryset=qs)
    qs_filtered = f.qs
    table = InventoryItemTable(qs_filtered)
    try:
        per_page = int(request.GET.get("per_page", 6))
    except ValueError:
        per_page = 6
    if per_page not in (6, 10, 25, 50, 100):
        per_page = 6
    RequestConfig(request, paginate={"per_page": per_page}).configure(table)
    return render(request, "inv/list_tables2.html", {
        "table": table,                    
        "filter": f,                       
        "current_project": current_project
    })

class InventoryListView(PermissionRequiredMixin,LoginRequiredMixin,SingleTableMixin, FilterView):
    permission_required = ["inv.view_inv", "inv.change_inv"]
    login_url = 'login/'
    model = InventoryItem
    table_class = InventoryItemTable
    template_name = "inv/list_tables2.html"
    filterset_class = InventoryItemFilter
    table_pagination = {
        "per_page": 6         
    }

    def get_table_pagination(self, table):
        try:
            per_page = int(self.request.GET.get("per_page", 6))
        except ValueError:
            per_page = 6
        if per_page not in (6, 10, 25, 50, 100):
            per_page = 6
        return {"per_page": per_page}

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(description__icontains=q)
        return qs


@login_required
@permission_required("inv.change_inv")
def inventory_create(request):
    project_code = request.GET.get("project") or request.POST.get("project")
    current_project = None
    if project_code:
        current_project = Project.objects.filter(code=project_code).first()

    if request.method == "POST":
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            obj = form.save(ommit=False)
            if current_project:
                obj.project = current_project
            obj.save()
            if request.headers.get("HX-Request"):
                return HttpResponse(status=204, headers={"HX-Refresh": "true"})
            per_page = 6
            total = InventoryItem.objects.count()
            last_page = math.ceil(total / per_page)
            return redirect(reverse("inv:list") + f"?page={last_page}#row-{obj.pk}")
    else:
        initial = {}
        if current_project:
            initial["project"] = current_project
        form = InventoryItemForm(initial=initial)

    if request.headers.get("HX-Request"):
        return render(request, "inv/inventory_form.html", {
            "form": form,
            "in_modal": True,
            "current_project": current_project
        })

    return render(request, "inv/create.html", {"form": form, "mode": "create", "current_project": current_project})

@login_required
@permission_required("inv.change_inv")
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

@login_required
@require_POST
@permission_required("inv.change_inv")
def inventory_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    item.delete()
    return redirect('inv:list')

def user_create(request):
    if request.method == "POST":
        usr = UsrCreation(request.POST)
        if usr.is_valid():
            usr.save()
            #messages.sucess(request, "User crated successfully")
            return redirect("inv:list")
    else:
        usr = UsrCreation()
    return render(request, "inv/usr_create.html", {"usr": usr})


@login_required
def HomeView(request):
    from .models import Project
    projects = Project.objects.order_by('label', 'code')
    return render(request, "inv/home.html",  {"projects": projects})
    # user = None
    # logout(request)
    # user = request.POST.get("username")
    # passw = request.POST.get("password")
    

    # #while not request.user.is_authenticated:
    # user = authenticate(request, username=user, password=passw)
    # if request.user.is_authenticated:
    #     login(request, user)
    #     return redirect("inv:list")
    # else:
    #     return HttpResponse("Invalid User")

# def register(request):
#     if request.method == 'POST':
#         form = UsrCreation(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, 'Account created')
#             return redirect('inv:login')
#     else:
#         form = UsrCreation()
#     return render(request, 'inv/register.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('inv:login')

def assign_permissions(request):
    User = get_user_model()
    users = User.objects.all()
