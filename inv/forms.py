
from django import forms
from .models import InventoryItem, CapexOpex, ItemType, Certification
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

            if isinstance(w, forms.Select):
                w.attrs['class'] = (w.attrs.get('class', '') + ' form-select').strip()
            else:
                # Inputs normales → form-control
                w.attrs['class'] = (w.attrs.get('class', '') + ' form-control').strip()

user = get_user_model()

class UsrCreation(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = user
        fields = ("username", "email", )

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ["certification_date", "file"]
        widgets = {
            "certification_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_file(self):
        f = self.cleaned_data["file"]
        max_mb = 10
        if f.size > max_mb * 1024 * 1024:
            raise forms.ValidationError(f"The file must not exceed {max_mb} MB.")
        import os
        allowed = {".pdf", ".png", ".jpg", ".jpeg"}
        ext = os.path.splitext(f.name)[1].lower()
        if ext not in allowed:
            raise forms.ValidationError("Allowed extensions: PDF, PNG, JPG, JPEG.")
        return f
