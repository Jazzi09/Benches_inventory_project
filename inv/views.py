
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.contrib.auth.models import User, Group
import math

from django_tables2 import SingleTableView
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django_tables2 import RequestConfig

from .models import InventoryItem, Project, SavedFilter
from .forms import InventoryItemForm, UsrCreation, CertificationForm
from .tables import InventoryItemTable, UsersTable
from .filters import InventoryItemFilter

from urllib.parse import parse_qs, urlencode


@login_required
@permission_required("inv.view_inv")
def inventory_filter_modal(request):

    project_code = request.GET.get("project")

    if project_code:
        current_project = Project.objects.filter(code=project_code).first()
        base_qs = (InventoryItem.objects
                   .filter(project=current_project)
                   .select_related('type', 'supplier', 'status', 'assigned_bench', 'project')
                   .order_by('id'))
        action = reverse("inv:inventory_by_project", args=[project_code])
    else:
        base_qs = (InventoryItem.objects
                   .select_related('type', 'supplier', 'status', 'assigned_bench', 'project')
                   .order_by('id'))
        action = reverse("inv:list")

    f = InventoryItemFilter(request.GET, queryset=base_qs)

    if request.headers.get("HX-Request"):
        return render(request, "inv/filter_form.html", {
            "filter": f,
            "action_url": action,
            "project_code": project_code,
        })
    if project_code:
        return redirect("inv:inventory_by_project", project_code=project_code)
    return redirect("inv:list")

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
            action = reverse("inv:create")
            if current_project:
                action += f"?project={current_project.code}"  # preserva el proyecto
            return render(request, "inv/inventory_form.html", {
                "form": form,
                "in_modal": True,
                "action_url": action,
                "current_project": current_project,
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
            if request.headers.get("HX-Request"):
                return HttpResponse(status=204, headers={"HX-Refresh": "true"})
            return redirect("inv:list")
    else:
        form = InventoryItemForm(instance=item)

    if request.headers.get("HX-Request"):
        from django.urls import reverse
        action = reverse("inv:edit", args=[item.pk])
        return render(request, "inv/inventory_form.html", {
            "form": form,
            "in_modal": True,
            "action_url": action,
        })
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
    print("POST Payload:", request.POST.dict())
    
    group_name = request.POST.get("group")
    if not group_name:
        return HttpResponseBadRequest("Missing group")
    
    user = get_object_or_404(User, pk = user_id)
    group = get_object_or_404(Group, name=group_name)

    if request.user == user and not request.user.is_staff:
        return HttpResponseForbidden("You cannoy modify your own groups.")    
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

@login_required
@require_POST
def saved_filter_create(request):
    name = (request.POST.get("name") or "").strip()
    if not name:
        return render(request, "inv/saved_filter_form.html", {
            "error": "Name is required.",
        }, status=400)
    raw_qs = request.POST.get("current_qs", "")
    qs_dict = {}
    if raw_qs:
        for k, v in parse_qs(raw_qs, keep_blank_values=True).items():
            qs_dict[k] = v[0] if len(v) == 1 else v

    project_code = request.POST.get("project") or qs_dict.get("project") or None

    SavedFilter.objects.update_or_create(
        user=request.user,
        name=name,
        defaults={"params": qs_dict, "project_code": project_code}
    )

    return HttpResponse(status=204, headers={"HX-Trigger": "filtersSaved"})

@login_required
def saved_filter_list_modal(request):
    project_code = request.GET.get("project")
    objects = SavedFilter.objects.filter(user=request.user).order_by("-created_at")

    items = []
    for f in objects:
        params = f.params or {}
        qs = urlencode(params, doseq=True)
        items.append({"name": f.name, "qs": qs})

    return render(request, "inv/saved_filter_dropdown.html", {
        "project_code": project_code,
        "items": items,
    })

@login_required
def saved_filter_form_modal(request):
    project_code = request.GET.get("project")
    current_qs = request.META.get("QUERY_STRING", "")
    ctx = {
        "project": project_code,
        "current_qs": current_qs,
    }
    return render(request, "inv/saved_filter_form.html", ctx)
