from django import forms
from .models import *

class CustomerForm(forms.ModelForm):
    # Define choices for terms_of_payment field
    TERMS_OF_PAYMENT_CHOICES = (
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
    )
    terms_of_payment = forms.ChoiceField(choices=TERMS_OF_PAYMENT_CHOICES)

    # Define choices for pengiriman field
    PENGIRIMAN_CHOICES = (
        (True, 'Yes'),
        (False, 'No'),
    )
    pengiriman = forms.ChoiceField(choices=PENGIRIMAN_CHOICES)

    npwp = forms.IntegerField(required=True)

    class Meta:
        model = Customer
        fields = '__all__'
        exclude=['cust_id']

class SupplierForm(forms.ModelForm):
    # Define choices for terms_of_payment field
    TERMS_OF_PAYMENT_CHOICES = (
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
    )
    terms_of_payment = forms.ChoiceField(choices=TERMS_OF_PAYMENT_CHOICES)
    npwp = forms.IntegerField(required=True)
    class Meta:
        model = Supplier
        fields = '__all__'
        exclude=['supp_id']

class CustPICForms(forms.ModelForm):
    Role_Options = (
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
    )
    Role = forms.ChoiceField(choices=Role_Options)

    class Meta:
        model = CustomerPIC
        fields = '__all__'
        exclude = ['customer_id']

class SuppPICForms(forms.ModelForm):
    Role_Options = (
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
    )
    Role = forms.ChoiceField(choices=Role_Options)

    class Meta:
        model = SupplierPIC
        fields = '__all__'
        exclude = ['supplier_id']

class CustAlamatForms(forms.ModelForm):
    class Meta:
        model = CustomerAlamat
        fields = '__all__'
        exclude = ['customer_id']

class SuppAlamattForms(forms.ModelForm):
    class Meta:
        model = SupplierAlamat
        fields = '__all__'
        exclude = ['supplier_id']

class ItemForm(forms.ModelForm):

    class Meta:
        model = Items
        fields = '__all__'
        exclude = ['SKU','gambar_resized']

class SumberForm(forms.ModelForm):

    class Meta:
        model = ItemSumber
        fields = '__all__'
        exclude = ['item']