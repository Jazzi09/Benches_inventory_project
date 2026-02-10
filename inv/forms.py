
from django import forms
from .models import InventoryItem, CapexOpex, ItemType
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
            'capex_opex': forms.RadioSelect(attrs={
                'class': 'form-check-input'
                }),
            'type': forms.RadioSelect(attrs={
                'class': 'form-check-input'
                }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'capex_opex' in self.fields:
            self.fields['capex_opex'].required = True
            self.fields['capex_opex'].empty_label = None
            self.fields['capex_opex'].queryset = CapexOpex.objects.order_by('label')
        if 'type' in self.fields:
            self.fields['type'].required = True
            self.fields['type'].empty_label = None
            self.fields['type'].queryset = ItemType.objects.order_by('label')

        for name, field in self.fields.items():
            w = field.widget
            if isinstance(w, (forms.RadioSelect, forms.CheckboxInput, forms.FileInput)):
                continue
            w.attrs['class'] = (w.attrs.get('class', '') + ' form-control').strip()

        
        self.fields.get('cft_number', {}).widget.attrs.setdefault('placeholder', 'CFT #')
        self.fields.get('pr_number', {}).widget.attrs.setdefault('placeholder', 'PR #')
        self.fields.get('po_number', {}).widget.attrs.setdefault('placeholder', 'PO #')
        self.fields.get('wo_number', {}).widget.attrs.setdefault('placeholder', 'WO')
        self.fields.get('invoice_id', {}).widget.attrs.setdefault('placeholder', 'Invoice ID')



user = get_user_model()

class UsrCreation(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = user
        fields = ("username", "email", )