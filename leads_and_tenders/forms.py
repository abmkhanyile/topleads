from django import forms
from . import models

class TenderForm(forms.ModelForm):
    class Meta:
        model = models.Tender
        exclude = (
            'tenderCategory',
            'tenderProvince',
            'assigned_keywords',
            'created_at',
        )
        fields = '__all__'

        widgets = {
            'buyersName': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'summary': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'refNum': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'issueDate': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'closingDate': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'siteInspectionDate': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'siteInspectionDate': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'enquiries': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'tender_docs': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            
        }
