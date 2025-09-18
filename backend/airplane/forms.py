from django import forms
from .models import *

class GateForm(forms.ModelForm):
    class Meta:
        model = Gate
        fields = ['id', 'size']

class RunwayForm(forms.ModelForm):
    class Meta:
        model = Runway
        fields = ['id', 'size']

class AirportForm(forms.ModelForm):
    class Meta:
        model = Airport
        #fields = ['name', 'location', 'gates', 'runways']
        fields = ['name', 'gates', 'runways']

class AirplaneForm(forms.ModelForm):
    class Meta:
        model = Airplane
        #fields = ['id', 'location', 'size', 'capacity', 'headingX', 'headingY', 'speed']
        fields = ['id', 'size', 'maxPassenger']

class AirlineForm(forms.ModelForm):
    class Meta:
        model = Airline
        fields = ['name', 'airplanes', 'airports']