from django import forms
from .models import Cell, Zone

class CellForm(forms.ModelForm):
    zone = forms.ModelChoiceField(queryset=Zone.objects.all(), empty_label=None)

    class Meta:
        model = Cell
        fields = '__all__'
class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = '__all__'
