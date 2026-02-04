from django.urls import path
from .views import InventoryListView, inventory_create, inventory_edit, inventory_delete

app_name = "inv"
urlpatterns = [
    path('inventory/', InventoryListView.as_view(), name='list'),
    path('new/', inventory_create, name='create'),
    path("<int:pk>/edit/", inventory_edit, name="edit"),
    path("<int:pk>/delete/", inventory_delete, name="delete"),
]
