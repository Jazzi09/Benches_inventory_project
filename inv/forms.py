
from django import forms
from .models import InventoryItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 2,
                "cols": 40,
            }),
            "comments": forms.Textarea(attrs={
                "rows": 2,
                "cols": 40,
            }),
        }

user = get_user_model()

class UsrCreation(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = user
        fields = ("username", "email", )