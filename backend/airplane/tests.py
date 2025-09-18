import datetime
from django.utils import timezone
from django.test import TestCase
from .models import Airport, GateRunwayAssignment, Airplane, Gate, PassengerAssignment, Runway, TakeOffRequest
from .datachecks import smallerThan, getDirectionTo, assignToGateOrRunway, handleTakeOffRequest, addPassengers
from .datachecks import Error
from unittest.mock import patch

# Test the 'smallerThan' function
class TestSmallerThanFunction(TestCase):
    def test_smaller_than(self):
        self.assertTrue(smallerThan("SMALL", "MEDIUM"))
        self.assertTrue(smallerThan("SMALL", "LARGE"))
        self.assertFalse(smallerThan("MEDIUM", "SMALL"))
        self.assertFalse(smallerThan("LARGE", "SMALL"))
        self.assertFalse(smallerThan("LARGE", "MEDIUM"))


# Test the 'getDirectionTo' function for calculating correct heading
class TestGetDirectionToFunction(TestCase):
    def test_get_direction_to(self):
        og = Airport.objects.create(x=0, y=0)  # Origin airport at (0, 0)
        
        dest = Airport.objects.create(x=1, y=1)
        self.assertEqual(getDirectionTo(og, dest), 315)     # Should return 315 degrees (north-east)

        dest2 = Airport.objects.create(x=-1, y=1)
        self.assertEqual(getDirectionTo(og, dest2), 225)    # Should return 225 degrees (north-west)

        dest3 = Airport.objects.create(x=-1, y=-1)
        self.assertEqual(getDirectionTo(og, dest3), 135)    # Should return 135 degrees (south-west)

        dest4 = Airport.objects.create(x=1, y=-1)
        self.assertEqual(getDirectionTo(og, dest4), 45)     # Should return 45 degrees (south-east)


# Test the 'assignToGateOrRunway' function for error handling
class TestAssignToGateOrRunway(TestCase):
    @patch('airplane.datachecks.create_error_response')  # Patch the create_error_response function
    def test_duplicate_gate(self, mock_create_error_response):
        # Setup the objects
        plane1 = Airplane.objects.create(id="Plane1", size="MEDIUM", maxPassenger=150, currentPassengerCount=0)
        plane2 = Airplane.objects.create(id="Plane2", size="LARGE", maxPassenger=200, currentPassengerCount=0)
        gate = Gate.objects.create(id="Gate1", size="SMALL")
        runway = Runway.objects.create(id="Runway1", size="LARGE")

        arrive_at_time = timezone.make_aware(datetime.datetime(2024, 11, 16, 12, 0, 0))

        # Create the first GateRunwayAssignment
        GateRunwayAssignment.objects.create(plane=plane1, gate=gate, runway=runway, arrive_at_time=arrive_at_time)

        # Call the function to test for duplicate gate assignment
        assignToGateOrRunway(GateRunwayAssignment.objects.create(plane=plane2, gate=gate, runway=runway, arrive_at_time=arrive_at_time))

        # Assert that the create_error_response function was called
        mock_create_error_response.assert_called_with(
            Error.DUPLICATE_GATE, "GATE", gate.id, True
        )

    @patch('airplane.datachecks.create_error_response')
    def test_duplicate_runway(self, mock_create_error_response):
        plane1 = Airplane.objects.create(id="Plane1", size="MEDIUM", maxPassenger=150, currentPassengerCount=0)
        plane2 = Airplane.objects.create(id="Plane2", size="LARGE", maxPassenger=200, currentPassengerCount=0)
        gate1 = Gate.objects.create(id="Gate1", size="MEDIUM")
        gate2 = Gate.objects.create(id="Gate2", size="MEDIUM")
        
        arrive_at_time = timezone.make_aware(datetime.datetime(2024, 11, 16, 12, 0, 0))
        runway = Runway.objects.create(id="Runway1", size="LARGE")

        # Create initial assignment
        GateRunwayAssignment.objects.create(plane=plane1, gate=gate1, runway=runway, arrive_at_time=arrive_at_time)

        # Try to assign the same runway to another plane (should trigger an error)
        assignToGateOrRunway(GateRunwayAssignment.objects.create(plane=plane2, gate=gate2, runway=runway, arrive_at_time=arrive_at_time))
        
        # Check for a DUPLICATE_RUNWAY error in the log
        mock_create_error_response.assert_called_with(
            Error.DUPLICATE_RUNWAY, "RUNWAY", runway.id, True
        )

    @patch('airplane.datachecks.create_error_response')
    def test_too_small_gate(self, mock_create_error_response):
        plane = Airplane.objects.create(id="Plane1", size="LARGE", maxPassenger=200, currentPassengerCount=0)
        gate = Gate.objects.create(id="Gate1", size="SMALL")
        
        arrive_at_time = timezone.make_aware(datetime.datetime(2024, 11, 16, 12, 0, 0))
        runway = Runway.objects.create(id="Runway1", size="LARGE")

        # Create assignment where gate is too small for plane1        
        assignToGateOrRunway(GateRunwayAssignment.objects.create(plane=plane, gate=gate, runway=runway, arrive_at_time=arrive_at_time))

        # Check for a TOO_SMALL_GATE error in the log
        mock_create_error_response.assert_called_with(
            Error.TOO_SMALL_GATE, "GATE", gate.size, True
        )

    @patch('airplane.datachecks.create_error_response')
    def test_too_small_runway(self, mock_create_error_response):
        plane = Airplane.objects.create(id="Plane1", size="LARGE", maxPassenger=200, currentPassengerCount=0)
        gate = Gate.objects.create(id="Gate1", size="LARGE")
        
        arrive_at_time = timezone.make_aware(datetime.datetime(2024, 11, 16, 12, 0, 0))
        runway = Runway.objects.create(id="Runway1", size="SMALL")

        # Create assignment where runway is too small for plane2
        assignment = GateRunwayAssignment.objects.create(plane=plane, gate=gate, runway=runway, arrive_at_time=arrive_at_time)
        assignToGateOrRunway(assignment)

        mock_create_error_response.assert_called_with(
            Error.TOO_SMALL_RUNWAY, "RUNWAY", runway.size, True
        )

class TestHandleTakeOffRequest(TestCase):
    @patch('airplane.datachecks.create_error_response')
    def test_wrong_airport(self, mock_create_error_response):
        # Create test airports
        Airport.objects.create(name="Airport1", x=0, y=0)
        Airport.objects.create(name="Airport2", x=10, y=10)

        # Create an airplane
        airplane = Airplane.objects.create(id="Plane1", size="LARGE", maxPassenger=200, currentPassengerCount=0)

        # Create a TakeOffRequest where the origin and destination do not match the plane's heading
        request = TakeOffRequest.objects.create(
            plane=airplane,
            origin="Airport1",
            destination="Airport2",
            direction=45,  # Incorrect direction to simulate an error
            speed=300,     # Provide a valid speed value
            landing_time=timezone.now() + timezone.timedelta(minutes=30),
            take_off_time=timezone.now()  # Add a value for take_off_time
        )

        # Call the function to check for the wrong airport error
        handleTakeOffRequest(request)

        # Check that create_error_response was called with the correct parameters
        mock_create_error_response.assert_called_with(
            Error.WRONG_AIRPORT, "PLANE", airplane.id, True
        )

class TestAddPassengersFunction(TestCase):
    @patch('airplane.datachecks.create_error_response')  # Patch the create_error_response function
    def test_too_many_passengers(self, mock_create_error_response):
        # Setup the objects
        plane = Airplane.objects.create(id="Plane1", size="MEDIUM", maxPassenger=150, currentPassengerCount=0)
                
        # Call the function to test for too many passengers
        addPassengers(PassengerAssignment.objects.create(plane=plane, passenger_count=160))

        # Assert that the create_error_response function was called
        mock_create_error_response.assert_called_with(
            Error.TOO_MANY_PASSENGERS, "PLANE", plane.id, True
        )

class TestHandleCollisionImminent(TestCase):
    @patch('airplane.datachecks.create_error_response')  # Patch the create_error_response function
    def test_collision_imminent(self, mock_create_error_response):
        # Setup the objects
        plane1 = Airplane.objects.create(id="Plane1", size="MEDIUM", maxPassenger=150, currentPassengerCount=0)
        plane2 = Airplane.objects.create(id="Plane2", size="LARGE", maxPassenger=200, currentPassengerCount=0)
        Runway.objects.create(id="Runway1", size="LARGE")

        Airport.objects.create(name="JFK", x=0, y=0)
        Airport.objects.create(name="LAX", x=10, y=10)
        
        # Create TakeOffRequest for both planes at the same time (collision scenario)
        TakeOffRequest.objects.create(
            plane=plane1,
            origin="JFK",
            destination="LAX",
            direction=315,
            speed=500,
            landing_time=timezone.now() + timezone.timedelta(minutes=30),
            take_off_time=timezone.now()  # Add a value for take_off_time
        )
        
        tor_to_compare = TakeOffRequest.objects.create(
            plane=plane2,
            origin="LAX",
            destination="JFK",
            direction=135,
            speed=500,
            landing_time=timezone.now() + timezone.timedelta(minutes=30),
            take_off_time=timezone.now()  # Add a value for take_off_time
        )
        
        # Call the function to test for collision imminent error
        handleTakeOffRequest(tor_to_compare)  # We check for collisions when tor2 is processed

        # Assert that the create_error_response function was called
        mock_create_error_response.assert_called_with(
            Error.COLLISION_IMMINENT, "PLANE", plane2.id, True
        )