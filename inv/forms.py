
from django import forms
from .models import InventoryItem

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
