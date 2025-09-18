# Function Library for analyzing data recieved from 
# Evently payloads and calculating error responses

from .models import *
from enum import Enum
import math

class Error(Enum):
    DUPLICATE_GATE = 1
    DUPLICATE_RUNWAY = 2
    WRONG_AIRPORT = 3
    TOO_MANY_PASSENGERS = 4
    TOO_SMALL_GATE = 5
    TOO_SMALL_RUNWAY = 6
    COLLISION_IMMINENT = 7

# compares size fields from database
def smallerThan(size1:str, size2:str):
    if (size1 == "SMALL" and size2 != "SMALL"):
        return True
    elif (size1 == "MEDIUM" and size2 == "LARGE"):
        return True
    return False

# returns the correct heading to get from pointA to pointB in degrees (0 to 360)
def getDirectionTo(og, dest):
    theta = math.degrees(math.atan2(og.x - dest.x, og.y - dest.y))
    return (theta + 90) % 360

def assignToGateOrRunway (assignment: GateRunwayAssignment):
    for GRA in GateRunwayAssignment.objects.all():
        # check for duplicate gate assignment
        if (GRA.gate == str(assignment.gate)) and (GRA.plane != str(assignment.plane)):
            create_error_response(Error.DUPLICATE_GATE, "GATE", assignment.gate.id, True)
            return
        # check for duplicate runway assignment
        if (GRA.runway == str(assignment.runway)) and (GRA.plane != str(assignment.plane)):
            create_error_response(Error.DUPLICATE_RUNWAY, "RUNWAY", assignment.runway.id, True)
            return
        
    # double nested for loop :(
    for plane in Airplane.objects.all():
        for gate in Gate.objects.all():
            # check if assigned gate is too small
            if (plane.id == assignment.plane.id) and (gate.id == assignment.gate.id) and (smallerThan(gate.size, plane.size)):
                create_error_response(Error.TOO_SMALL_GATE, "GATE", assignment.gate.size, True)
                return
        for runway in Runway.objects.all():
            # check if assigned runway is too small
            if (plane.id == assignment.plane.id) and (runway.id == assignment.runway.id) and (smallerThan(runway.size, plane.size)):
                create_error_response(Error.TOO_SMALL_RUNWAY, "RUNWAY", assignment.runway.size, True)
                return 


def handleTakeOffRequest(request: TakeOffRequest):
    # need to get x and y of airports
    dir = 0
    try: 
        og = Airport.objects.get(name=request.origin)
        dest = Airport.objects.get(name=request.destination)
        dir = round(getDirectionTo(og, dest))
    except Airport.DoesNotExist:
        # not a valid error: we can assume this won't happen
        print("Airport does not exist")
        return

    if (dir != request.direction):
        create_error_response(Error.WRONG_AIRPORT, "PLANE", request.plane.id, True)
        return
    
    # collision detection - oversimplified for now
    for TOR in TakeOffRequest.objects.all():
        if (TOR.landing_time == request.landing_time) and (TOR.destination == request.destination):
            create_error_response(Error.COLLISION_IMMINENT, "PLANE", request.plane.id, True)
            return

# takes a passenger assignment and uses it to add passengers to a 
# plane, calling create_error_response if the plane is too small
def addPassengers (assignment: PassengerAssignment):
    for plane in Airplane.objects.all():
        if plane.id == assignment.plane.id:
            plane.currentPassengerCount += assignment.passenger_count
            plane.save()
            if ((assignment.passenger_count + plane.currentPassengerCount) > plane.maxPassenger):
                create_error_response(Error.TOO_MANY_PASSENGERS, "PLANE", plane.id, True)
    return

# creates a correctly-formatted JSON error response but doesnt do anything with it yet
def create_error_response(errtype: Error, objType: str, id, debugMode: bool = False):
    response =  ("{\n" +
        "\"team_id\": \"id_issued_by_evently\"\n" +
        f"\"obj_type\": \"{objType}\"\n" +
        f"\"id\": \"{id}\"\n" +
        f"\"error\": \"{errtype}\"\n" +
        "}")
    
    if (debugMode):
        print(f"\nERROR: {errtype}\n")
        print(response)

    return response