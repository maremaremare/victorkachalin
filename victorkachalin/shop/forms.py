# coding: utf-8
from django.forms import ModelForm
from shop.models import Order
from django import forms

class OrderForm(ModelForm):
    class Meta:
        model = Order
        #fields = ['name', 'email', 'address', 'phone', 'merchandise_id', 'extra_field']
    CHOICES=[
         ('select 1','Получу при личной встрече в Москве на м. Теплый Стан'), ('select 2','Доставка почтой России'), ]

    delivery = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect() )
    address = forms.CharField(required = False)
    #merchandise_id = forms.CharField( required=False)
    extra_field = forms.CharField(required = False)   

form = OrderForm(initial={'delivery': 'select 1'})