from django import forms
from . import models
from leads_and_tenders.models import Province, Category, Keywords


class SP_Form1(forms.Form):
    trading_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter the name of the business'
    }))
    regnum = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter business registration number'
    }))
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter business address'
    }))
    contact_num = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter business contact number'
    }))


class SP_Form2(forms.Form):
    sp_type = forms.TypedChoiceField(
        choices=models.TYPE,
        coerce=int,
        required=True,
        label="Select your business type",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select Service Provider'
        })
    )
    provinces = forms.ModelMultipleChoiceField(
        queryset=Province.objects.all(), 
        required=True,
        label="Select provinces of interest", 
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control biz-provinces',
            'multiple': 'multiple',
        })
    )
    business_categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), 
        required=True, 
        label="Select your business category",
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control biz-categories',
            'multiple': 'multiple',
        })
    )
    business_keywords = forms.CharField(
        # queryset=Keywords.objects.none(), 
        required=False, 
        label="What are your business keywords", 
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control biz-keywords',
            'multiple': 'multiple',
        })
    )