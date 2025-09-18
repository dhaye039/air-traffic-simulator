from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import LogoutView

from .models import *
from .forms import *
# perms debugging
from django.contrib.auth.models import Group, Permission, User
from django.contrib.auth import get_user_model

# rest api
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GateRunwayAssignmentSerializer, TakeOffRequestSerializer, PassengerAssignmentSerializer
from .datachecks import *

import logging
logger = logging.getLogger(__name__)

# TODO: create a login page to redirect to
@login_required
def hello(request):
    template = loader.get_template('homepage.html')
    return HttpResponse(template.render())

def exampleDisplay(request):
    mytests = TestModel.objects.all().values()
    template = loader.get_template('testdisplay.html')
    context = {
        'mytests': mytests,
    }
    return HttpResponse(template.render(context, request))

def gateDisplay(request):
    gates = Gate.objects.all()
    template = loader.get_template('gatedisplay.html')
    context = {
        'mygates': gates,
    }
    return HttpResponse(template.render(context, request))

def runwayDisplay(request):
    runways = Runway.objects.all()
    template = loader.get_template('runwaydisplay.html')
    context = {
        'myrunways': runways,
    }
    return HttpResponse(template.render(context, request))

def airportDisplay(request):
    aps = Airport.objects.all()
    template = loader.get_template('airportdisplay.html')
    context = {
        'myairports': aps,
    }
    return HttpResponse(template.render(context, request))

def airplaneDisplay(request):
    planes = Airplane.objects.all()
    template = loader.get_template('airplanedisplay.html')
    context = {
        'myairplanes': planes,
    }
    return HttpResponse(template.render(context, request))

def airlineDisplay(request):
    airlines = Airline.objects.all()
    template = loader.get_template('airlinedisplay.html')
    context = {
        'myairlines': airlines,
    }
    return HttpResponse(template.render(context, request))

def logoutView (request):
    logger.debug("CustomLogoutView GET method called")
    template = loader.get_template('registration/logout.html')
    return HttpResponse(template.render())

# DATA INSERTION--------------------------------------------------------------------------
@permission_required('auth.canInsertData', raise_exception=True)
def addgate(request):
    if request.method == 'POST':
        form = GateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gate display')  # Redirect to the page that lists all gates
    else:
        form = GateForm()
    return render(request, 'dataInsertion/addgate.html', {'form': form})

@permission_required('auth.canInsertData', raise_exception=True)
def addrunway(request):
    if request.method == 'POST':
        form = RunwayForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('runway display')  # Redirect to the page that lists all runways
    else:
        form = RunwayForm()
    return render(request, 'dataInsertion/addrunway.html', {'form': form})

@permission_required('auth.canInsertData', raise_exception=True)
def addairport(request):
    if request.method == 'POST':
        form = AirportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('airport display')  # Redirect to the page that lists all airports
    else:
        form = AirportForm()
    return render(request, 'dataInsertion/addairport.html', {'form': form})

@permission_required('auth.canInsertData', raise_exception=True)
def addairplane(request):
    if request.method == 'POST':
        form = AirplaneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('airplane display')  # Redirect to the page that lists all airports
    else:
        form = AirplaneForm()
    return render(request, 'dataInsertion/addairplane.html', {'form': form})

@permission_required('auth.canInsertData', raise_exception=True)
def addairline(request):
    if request.method == 'POST':
        form = AirlineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('airline display')  # Redirect to the page that lists all airports
    else:
        form = AirlineForm()
    return render(request, 'dataInsertion/addairline.html', {'form': form})

# DATA DELETION--------------------------------------------------------------------------
@permission_required('auth.canDeleteData', raise_exception=True)
def deletegate(request):
    msg = ""
    if request.method == 'POST':
        gateId = request.POST["gate_id"]
        try:
            gateInstance = Gate.objects.get(id=gateId)
            gateInstance.delete()
            msg = "successfully deleted gate with id: " + str(gateId)
        except Gate.DoesNotExist:
            msg = "gate with id: " + str(gateId) + " does not exist"
    
    return render(request, 'dataDeletion/deletegate.html', {'msg': msg})

@permission_required('auth.canDeleteData', raise_exception=True)
def deleterunway(request):
    msg = ""
    if request.method == 'POST':
        runwayID = request.POST["runway_id"]
        try:
            runwayInstance = Runway.objects.get(id=runwayID)
            runwayInstance.delete()
            msg = "successfully deleted runway with id: " + str(runwayID)
        except Runway.DoesNotExist:
            msg = "runway with id: " + str(runwayID) + " does not exist"
    
    return render(request, 'dataDeletion/deleterunway.html', {'msg': msg})

@permission_required('auth.canDeleteData', raise_exception=True)
def deleteairport(request):
    msg = ""
    if request.method == 'POST':
        airportID = request.POST["airport_id"]
        try:
            airportInstance = Airport.objects.get(name=airportID)
            airportInstance.delete()
            msg = "successfully deleted airport with name: " + str(airportID)
        except Airport.DoesNotExist:
            msg = "airport with name: " + str(airportID) + " does not exist"
    
    return render(request, 'dataDeletion/deleteairport.html', {'msg': msg})

@permission_required('auth.canDeleteData', raise_exception=True)
def deleteairplane(request):
    msg = ""
    if request.method == 'POST':
        airplaneID = request.POST["airplane_id"]
        try:
            airplaneInstance = Airplane.objects.get(id=airplaneID)
            airplaneInstance.delete()
            msg = "successfully deleted airplane with id: " + str(airplaneID)
        except Airplane.DoesNotExist:
            msg = "airplane with id: " + str(airplaneID) + " does not exist"
    
    return render(request, 'dataDeletion/deleteairplane.html', {'msg': msg})

@permission_required('auth.canDeleteData', raise_exception=True)
def deleteairline(request):
    msg = ""
    if request.method == 'POST':
        airlineID = request.POST["airline_id"]
        try:
            airlineInstance = Airline.objects.get(name=airlineID)
            airlineInstance.delete()
            msg = "successfully deleted airline with name: " + str(airlineID)
        except Airline.DoesNotExist:
            msg = "airline with name: " + str(airlineID) + " does not exist"
    
    return render(request, 'dataDeletion/deleteairline.html', {'msg': msg})


# REST API------------------------------------------------------------------------------
class TakeOffRequests(APIView):
    def get(self, request):
        TORs = TakeOffRequest.objects.all()
        serializer = TakeOffRequestSerializer(TORs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TakeOffRequestSerializer(data=request.data)
        if serializer.is_valid():
            TOR = serializer.save()
            # check for errors in database
            handleTakeOffRequest(TOR)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # TODO return json error response 

class GateRunwayAssignments(APIView):
    def get(self, request):
        GRAs = GateRunwayAssignment.objects.all()
        serializer = GateRunwayAssignmentSerializer(GRAs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GateRunwayAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            GRA = serializer.save()
            # method from data_checks.py
            assignToGateOrRunway(GRA)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PassengerAssignments(APIView):
    def get(self, request):
        PAs = PassengerAssignment.objects.all()
        serializer = PassengerAssignmentSerializer(PAs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PassengerAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            PA = serializer.save()
            # method from data_checks.py
            addPassengers(PA)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# For permission checking debugging; ignore this
def checkPerms(request):
    user = get_user_model().objects.get(username='steve')
    user.user_permissions.clear()
    user = get_user_model().objects.get(username='steve')
    user = User.objects.get(username='steve')
    user.refresh_from_db()

    if user.has_perm('auth.canInsertData'):
        print("User has the permission: auth.canInsertData")
    else:
        print("User does not have the permission")
    if user.groups.filter(name='ElevatedPrivilegeUsers').exists():
        print("User is in the group")
    else:
        print("User is not in the group")

    group = Group.objects.get(name='ElevatedPrivilegeUsers')
    permission = Permission.objects.get(codename='canInsertData')

    if group.permissions.filter(id=permission.id).exists():
        print("Group has the permission")
    else:
        print("Group does not have the permission")

    template = loader.get_template('homepage.html')
    return HttpResponse(template.render())