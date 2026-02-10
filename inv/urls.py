from django.urls import path
from django.contrib.auth import views as auth_views
from .views import InventoryListView, inventory_create, inventory_edit, inventory_delete, user_create, HomeView, log_out, inventory_by_project

app_name = "inv"
urlpatterns = [
    path('inventory/', InventoryListView.as_view(), name='list'),
    path('home', HomeView, name='home_view'),
    path('inventory/<str:project_code>/', inventory_by_project, name='inventory_by_project'),
    path('new/', inventory_create, name='create'),
    path("<int:pk>/edit/", inventory_edit, name="edit"),
    path("<int:pk>/delete/", inventory_delete, name="delete"),
    path("usr_create/", user_create, name='usr_create'),
    path('login/', auth_views.LoginView.as_view(template_name="inv/login.html"), name='login'),
    path('logout/', log_out, name='logout'),
]
