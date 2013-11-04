# coding: utf-8
import re
from django import forms
from django.forms import ModelForm
from django.forms.models import fields_for_model
from shop.models import Order


class PhoneField(forms.Field):
    phoneMatchRegex = re.compile(r"^\d{10}$")
    phoneSplitRegex = re.compile(r"^\d{10}$")
 
    def clean(self, value):
        if not value:
            return ""
        if not self.phoneMatchRegex.match(value):
            raise forms.ValidationError("Неверный телефонный номер. Введите десятизначный номер (без восьмерки)")
        
 
        # Always return the cleaned data.
        return value

class OrderForm(ModelForm):
    class Meta:
        model = Order
        #fields = ['name', 'email', 'address', 'phone', 'merchandise_id', 'extra_field']
    CHOICES=[
         ('select 1','Получу при личной встрече в Москве на м. Теплый Стан'), ('select 2','Доставка почтой России'), ]

    delivery = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect() )
    address = forms.CharField(required = False, label ='Адрес')
    #merchandise_id = forms.CharField( required=False)
    phone = PhoneField(required = True)
    extra_field = forms.CharField(required = False)   
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs['pattern'] = "[0-9]{10}"
        self.fields['phone'].widget.attrs['placeholder'] = "9651112233"
        self.fields['phone'].label = 'Телефон'
        self.fields['delivery'].label = 'Доставка'
        self.fields['name'].label = 'Имя'
        self.fields['email'].label = 'E-mail'

class EditOrderForm(OrderForm):
    class Meta:
        model = Order
        exclude = ('order_id','merchandise_id', 'extra_field', 'created_at', 'photo_id', 'postal', 'meeting')


form = OrderForm(initial={'delivery': 'select 1'})

