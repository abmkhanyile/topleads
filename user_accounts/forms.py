from django.forms import ModelForm
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation



class CustomUserForm(UserCreationForm):
    password1 = forms.CharField(label="", help_text=password_validation.password_validators_help_text_html(), widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password'
    }))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password'
    }))
    class Meta:
        model = CustomUser
        exclude = (
            "terms",
        )
        fields = (
            "email",
            "first_name",
            "last_name",
            "contactNumber",
            "password1",
            "password2",
        )

        labels = {
            'email': '',
            'first_name': '',
            'last_name': '',
            'contactNumber': '',
        }
     
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }),
            'contactNumber': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact Number',
            }),
            'terms': forms.CheckboxInput(),
        }

    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']

        if commit:
            user.save()

        return user



class PayFast_Form(forms.Form):
    merchant_id = forms.CharField(widget=forms.HiddenInput())

    merchant_key = forms.CharField(widget=forms.HiddenInput())

    return_url = forms.CharField(widget=forms.HiddenInput())

    cancel_url = forms.CharField(widget=forms.HiddenInput())

    # notify_url = forms.CharField(widget=forms.HiddenInput())

    name_first = forms.CharField(widget=forms.HiddenInput())

    name_last = forms.CharField(widget=forms.HiddenInput())

    email_address = forms.CharField(widget=forms.HiddenInput())

    cell_number = forms.CharField(widget=forms.HiddenInput())

    m_payment_id = forms.CharField(widget=forms.HiddenInput())

    amount = forms.CharField(widget=forms.HiddenInput())

    item_name = forms.CharField(widget=forms.HiddenInput())

    email_confirmation = forms.CharField(widget=forms.HiddenInput())

    confirmation_address = forms.CharField(widget=forms.HiddenInput())

    signature = forms.CharField(widget=forms.HiddenInput())