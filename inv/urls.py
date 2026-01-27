
from django.urls import path
from . import views

app_name = "inv"
urlpatterns = [
    path('', views.inventory_list, name='list'),
    path('new/', views.inventory_create, name='create'),
]
