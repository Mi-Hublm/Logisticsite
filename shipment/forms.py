from django import forms
from .models import Shipment

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['name', 'pick_up_location', 'drop_off_location', 'delivery_instructions', 'estimated_time', 'total_cost', 'items']
