from django import forms
from phonenumber_field.formfields import PhoneNumberField

from cart.models import Cart


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ["order_id", "contact_name", "contact_surname", "phone_number", "delivery_service",
                  "payment_type", "city"]

        widgets = {
            "payment_type": forms.Select(attrs={"class": "form-select form-select-lg"}),
            "delivery_service": forms.Select(attrs={"class": "form-select form-select-lg"}),
            "contact_name": forms.TextInput(attrs={"class": "form-control form-control-lg"}),
            "contact_surname": forms.TextInput(attrs={"class": "form-control form-control-lg"}),
            "city": forms.TextInput(attrs={"class": "form-control form-control-lg"}),
        }
    order_id = forms.CharField(label="Order id",
                               widget=forms.TextInput(attrs={'class': 'form-control form-control-lg',
                                                             'readonly': 'readonly'}))
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg",
                                                                  "placeholder": "+380984567823"}))
