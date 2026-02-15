from django.urls import path
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from .views import (
    InventoryListView, UserListView, inventory_create, inventory_edit, inventory_delete,
    user_create, HomeView, log_out, inventory_by_project, toggle_user_group, empty_path, 
    certification_history, certification_create
) 

app_name = "inv"
urlpatterns = [
    path('inventory/', InventoryListView.as_view(), name='list'),
    path('manage_users/', UserListView.as_view(), name="user_manage"),
    path('home', HomeView, name='home_view'),
    path('inventory/<str:project_code>/', inventory_by_project, name='inventory_by_project'),
    path('new/', inventory_create, name='create'),
    path("<int:pk>/edit/", inventory_edit, name="edit"),
    path("<int:pk>/delete/", inventory_delete, name="delete"),
    path("usr_create/", user_create, name='usr_create'),
    path("manage_users/<int:user_id>/toggle/", toggle_user_group, name="toggle_user_group"),
    path('login/', auth_views.LoginView.as_view(template_name="inv/login.html"), name='login'),
    path('logout/', log_out, name='logout'),
    path('', empty_path, name="empty_path"),
    path("items/<int:pk>/certifications", certification_history, name="certification_history"),
    path("items/<int:pk>/certification/new/", certification_create, name="certification_create"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
