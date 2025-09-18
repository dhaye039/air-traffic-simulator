from django.core.management import BaseCommand
from airplane.models import Airport, Airline, Gate, Runway, Airplane
import csv

class Command(BaseCommand):
    help = 'loads data into database if needed'

    def handle(self, *args, **options):
        loadedAirports = False
        loadedAirlines = False

        if Airport.objects.count() == 0:
            loadedAirports = True
            with open("airplane/datasets/airport.csv") as file:
                reader = csv.DictReader(file)
                for airport in reader:
                    Airport.objects.create(
                        name=airport["name"],
                        x=float(airport["x"]),
                        y=float(airport["y"])
                    )
            print("airports loaded")
        else:
            print("airports already loaded")

        if Airline.objects.count() == 0:
            loadedAirlines = True
            with open("airplane/datasets/airline.csv") as file:
                reader = csv.DictReader(file)
                for airline in reader:
                    Airline.objects.create(name=airline["name"])
            print("airlines loaded")
        else:
            print("airlines already loaded")

        if loadedAirports or loadedAirlines:
            with open("airplane/datasets/airport_airline.csv") as file:
                reader = csv.DictReader(file)
                for combo in reader:
                    Airline.objects.get(
                        name=combo["airline"]
                    ).airports.add(
                        Airport.objects.get(name=combo["airport"])
                    )
            print("airport / airlines loaded")
        else:
            print("airport / airlines already loaded")

        if Gate.objects.count() == 0:
            with open("airplane/datasets/gate.csv") as file:
                reader = csv.DictReader(file)
                for gate in reader:
                    Gate.objects.create(
                        id=gate["id"],
                        airport=Airport.objects.get(name=gate["airport"]),
                        size=gate["size"]
                    )
            print("gates loaded")
        else:
            print("gates already loaded")

        if Runway.objects.count() == 0:
            with open("airplane/datasets/runway.csv") as file:
                reader = csv.DictReader(file)
                for runway in reader:
                    Runway.objects.create(
                        id=runway["id"],
                        airport=Airport.objects.get(name=runway["airport"]),
                        size=runway["size"]
                    )
            print("runways loaded")
        else:
            print("runways already loaded")

        if Airplane.objects.count() == 0:
            with open("airplane/datasets/plane.csv") as file:
                reader = csv.DictReader(file)
                for plane in reader:
                    Airplane.objects.create(
                        id=plane["id"],
                        airline=Airline.objects.get(name=plane["airline"]),
                        size=plane["size"],
                        currentPassengerCount=0,
                        maxPassenger=plane["maxPassenger"]
                    )
            print("planes loaded")
        else:
            print("planes already loaded")