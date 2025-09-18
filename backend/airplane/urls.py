from django.urls import path
from . import views  # assuming your views are in the current directory

urlpatterns = [
    path('test/', views.exampleDisplay, name='exampleDisplay'),
    path('', views.hello, name='hello'),
    path('gatedisplay/', views.gateDisplay, name='gate display'),
    path('addgate/', views.addgate, name='add gate'),
    path('deletegate/', views.deletegate, name='delete gate'),
    path('runwaydisplay/', views.runwayDisplay, name='runway display'),
    path('addrunway/', views.addrunway, name='add runway'),
    path('deleterunway/', views.deleterunway, name='delete runway'),
    path('airportdisplay/', views.airportDisplay, name='airport display'),
    path('addairport/', views.addairport, name='add airport'),
    path('deleteairport/', views.deleteairport, name='delete airport'),
    path('airplanedisplay/', views.airplaneDisplay, name='airplane display'),
    path('addairplane/', views.addairplane, name='add airplane'),
    path('deleteairplane/', views.deleteairplane, name='delete airplane'),
    path('airlinedisplay/', views.airlineDisplay, name='airline display'),
    path('addairline/', views.addairline, name='add airline'),
    path('deleteairline/', views.deleteairline, name='delete airline'),
    path('pc/', views.checkPerms, name='check perms'),
    path('takeoffrequests/', views.TakeOffRequests.as_view()),
    path('gaterunwayassignments/', views.GateRunwayAssignments.as_view()),
    path('passengerassignments/', views.PassengerAssignments.as_view()),
]