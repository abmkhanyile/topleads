from django import forms
from .models import Company

#helps in creating a company
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = (
            'name',
            'reg_num',
            'address',
            'contact_num',
            'admins',
            'provinces',
            'categories',
            'keywords',
        )
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'reg_num': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'contact_num': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'admins': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'provinces': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'categories': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'keywords': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }