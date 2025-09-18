from django.db import models

# Create your models here.

# "Each model class represents a table in the database. 
# This file forms the foundation of your application's data management.""

SIZES = [
  ('LARGE', 'Size Large'),
  ('MEDIUM', 'Size Medium'),
  ('SMALL', 'Size Small'),
]


class TestModel(models.Model):
  name = models.CharField(max_length=255)
  otherAttribute = models.CharField(max_length=255)

class Airplane(models.Model):
  id = models.CharField(max_length=10, primary_key=True)
  #location = models.CharField(max_length=255)
  size = models.CharField(max_length=6, choices=SIZES)
  currentPassengerCount = models.PositiveIntegerField()
  maxPassenger = models.PositiveIntegerField()
  #capacity = models.PositiveIntegerField()
  #headingX = models.IntegerField()
  #headingY = models.IntegerField()
  #speed = models.DecimalField(max_digits=6, decimal_places=2, null=True)
  
  def __str__(self):
    return f"Airplane {self.id}, size: {self.size}, current passengers: {self.currentPassengerCount}, maxPassengers: {self.maxPassenger}"

class Gate(models.Model):
  id = models.CharField(max_length=10, primary_key=True)
  size = models.CharField(max_length=6, choices=SIZES)

  def __str__(self):
    return f"Gate {self.id} - size: {self.size}"

class Runway(models.Model):
  id = models.CharField(max_length=10, primary_key=True)
  size = models.CharField(max_length=6, choices=SIZES)

  def __str__(self):
    return f"Runway {self.id} - size: {self.size}"

class Airport(models.Model):
  name = models.CharField(max_length=255)
  #location = models.CharField(max_length=255)
  x = models.IntegerField()
  y = models.IntegerField()

  # relationships
  gates = models.ManyToManyField(Gate)
  runways = models.ManyToManyField(Runway)

  def __str__(self):
    return f"{self.name}, x: {self.x}, y: {self.y}"


class Airline(models.Model):
  name = models.CharField(max_length=255)
  # schema relationships
  airplanes = models.ManyToManyField(Airplane, blank=True)
  airports = models.ManyToManyField(Airport, blank=True)

  def __str__(self):
    return f"{self.name}"


# Data Recieved from Evently-----------------------------------
class TakeOffRequest(models.Model):
  direction = models.PositiveIntegerField()
  plane = models.CharField(max_length=10) #this has to be the name of a plane but I'll fix that later
  speed = models.DecimalField(max_digits=6, decimal_places=2)
  origin = models.CharField(max_length=3) #this has to be the name of an airport
  destination = models.CharField(max_length=3) #also has to be the name of an airport
  landing_time = models.DateTimeField()
  take_off_time = models.DateTimeField()

class GateRunwayAssignment(models.Model):
  plane = models.CharField(max_length=10) #has to be the name of a plane
  gate = models.CharField(max_length=10) #has to be the name of a gate
  runway = models.CharField(max_length=10) #has to be the name of a runway
  arrive_at_time = models.DateTimeField()

class PassengerAssignment(models.Model):
  plane = models.CharField(max_length=10) #has to be the name of a plane
  passenger_count = models.PositiveIntegerField()