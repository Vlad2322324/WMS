from django import forms
from .models import Cell, Zone

class CellForm(forms.ModelForm):
    class Meta:
        model = Cell
        fields = '__all__'

class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = '__all__'
