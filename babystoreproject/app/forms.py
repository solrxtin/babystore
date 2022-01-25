from django.forms import widgets
from .models import Item, Sale
from django import forms
from django.db.models.deletion import CASCADE


class ItemFormCRUD(forms.ModelForm):
    #department = forms.ForeignKey(Department, on_delete=CASCADE)
    name = forms.CharField(max_length=200)
    price = forms.IntegerField(required=True)
    quantity = forms.IntegerField(required=True)
    brand = forms.CharField(required=False)
    dozen_price = forms.IntegerField(required=False)
    

    class Meta:
        model = Item
        exclude = ('department',)


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        exclude = ['time_sold']

class NewSaleForm(forms.ModelForm):
    item = forms.CharField(max_length=50)
    price = forms.IntegerField(required=True)
    quantity = forms.IntegerField(required=True)
    class Meta:
        model=Sale
        exclude = ['time_sold']


class MultipleSaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        exclude = ['item', 'time_sold']


#print(obj.__dict__())


class SearchSaleForm(forms.ModelForm):
    search = forms.DateTimeField(widget=widgets.SelectDateWidget, label="Search sales by date")
    class Meta:
        model= Sale
        exclude = ["item", "price", "quantity"]


class UpdateCartForm(forms.ModelForm):
    quantity = forms.IntegerField(required=True)
    class Meta:
        model = Sale
        fields = ['quantity']