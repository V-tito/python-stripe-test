from django import forms
from . import models

class addToOrderForm(forms.Form):
    order=forms.ModelChoiceField(models.Order.objects.all(),blank=True)