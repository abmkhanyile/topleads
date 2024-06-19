from django import forms
# from .models import Testimonials
from leads_and_tenders.models import Category, Province

class TenderSearchForm(forms.Form):
    searchField = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'id': 'searchField_id',
        'class': 'search_field form-control',
        'placeholder': 'Search for tenders'
    }))

    categorySelectionField = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category",
                                                            widget=forms.Select(attrs={
                                                                'class': 'search_field form-control',                                                                
                                                            }))

    provinceSelectionField = forms.ModelChoiceField(queryset=Province.objects.all(), empty_label="Select Province", widget=forms.Select(attrs={
        'class': 'search_field form-control',
        
    }))



