from rest_framework import serializers
from .models import *

class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = '__all__'

class GateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gate
        fields = '__all__'

class RunwaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Runway
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__'

class TakeOffRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TakeOffRequest
        fields = '__all__'

class GateRunwayAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GateRunwayAssignment
        fields = '__all__'

class PassengerAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerAssignment
        fields = '__all__'