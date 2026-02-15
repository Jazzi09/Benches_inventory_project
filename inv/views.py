
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib.auth.models import User, Group
import math

from django_tables2 import SingleTableView
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django_tables2 import RequestConfig

from .models import InventoryItem, Project
from .forms import InventoryItemForm, UsrCreation, CertificationForm
from .tables import InventoryItemTable, UsersTable
from .filters import InventoryItemFilter


@login_required
def inventory_by_project(request, project_code):
    current_project = get_object_or_404(Project, code=project_code)
    qs = (InventoryItem.objects
          .filter(project=current_project)
          .select_related('type', 'supplier', 'status', 'assigned_bench')
          .order_by('id'))
    q = (request.GET.get("q") or "").strip()
    if q:
        qs = qs.filter(description__icontains=q)
    f = InventoryItemFilter(request.GET, queryset=qs)
    qs = f.qs
    try:
        per_page = int(request.GET.get("per_page", 6))
    except ValueError:
        per_page = 6
    if per_page not in (6, 10, 25, 50, 100):
        per_page = 6
    table = InventoryItemTable(qs)
    RequestConfig(request, paginate={"per_page": per_page}).configure(table)
    return render(request, "inv/list_tables2.html", {
        "table": table,                    
        "filter": f,                       
        "current_project": current_project
    })

class UserListView(LoginRequiredMixin,SingleTableMixin, FilterView):
    #permission_required = ["inv.view_inv", "inv.change_inv"],,, PermissionRequiredMixin
    login_url = 'login/'
    model = User
    table_class = UsersTable
    template_name = "inv/user_list.html"
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

class InventoryListView(LoginRequiredMixin,SingleTableMixin, FilterView):
    #permission_required = ["inv.view_inv", "inv.change_inv"],,,PermissionRequiredMixin
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
            return redirect("inv:login")
    else:
        usr = UsrCreation()
    return render(request, "inv/usr_create.html", {"usr": usr})

@login_required
def HomeView(request):
    from .models import Project
    projects = Project.objects.order_by('label', 'code')
    return render(request, "inv/home.html",  {"projects": projects})

def log_out(request):
    logout(request)
    return redirect('inv:login')

def toggle_user_group(request, user_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

        #return redirect("inv:user_manage")
    print("POST Payload:", request.POST.dict())
    
    group_name = request.POST.get("group")
    if not group_name:
        return HttpResponseBadRequest("Missing group")
    
    user = get_object_or_404(User, pk = user_id)
    group = get_object_or_404(Group, name=group_name)

    if request.user == user and not request.user.is_staff:
        return HttpResponseForbidden("You cannoy modify your own groups.")
        #return redirect("inv:user_manage")
    
    if group in user.groups.all():
        user.groups.remove(group)
        messages.info(request, f"Removed {user.username} from {group.name} ")
    else:
        user.groups.add(group)
        messages.info(request, f"Added {user.username} to {group.name} ")

    return redirect(request.POST.get("next")) or reverse ("inv:user_manage")

def empty_path(request):
    return redirect("inv:home_view")

def logged_in(request):
    return redirect("inv:home_view")

@login_required
@permission_required("inv.view_inv")
def certification_history(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    certifications = item.certifications.all().order_by("-certification_date")
    project_code = item.project.code if item.project else None
    return render(
        request,
        "inv/certification_history.html",
        {
            "item": item,
            "certifications": certifications,
            "project_code": project_code,
        },
)

@login_required
@permission_required("inv.change_inv")
def certification_create(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if not item.requires_certification:
        messages.error(request, "This item does not require certification.")
        return redirect("inv:certification_history", pk=item.pk)

    if request.method == "POST":
        form = CertificationForm(request.POST, request.FILES)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.item = item
            cert.save()
            messages.success(request, "Certification saved successfully.")
            return redirect("inv:certification_history", pk=item.pk)
    else:
        form = CertificationForm()

    return render(request, "inv/certification_form.html", {"item": item, "form": form})