from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    InventoryListView, UserListView, inventory_create, inventory_edit, inventory_delete,
    user_create, HomeView, log_out, inventory_by_project, toggle_user_group, empty_path, 
    logged_in, certification_history, certification_create, inventory_filter_modal,
    saved_filter_modal, saved_filter_create, saved_filter_list_modal
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
    path("accounts/profile/", logged_in, name="logged_in"),
    path("filters/modal/", inventory_filter_modal, name="filter_modal"),
    path("filters/save/modal/", saved_filter_modal, name="saved_filter_modal"),
    path("filters/save/", saved_filter_create, name="saved_filter_create"),
    path("filters/saved/modal/", saved_filter_list_modal, name="saved_filter_list_modal"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
