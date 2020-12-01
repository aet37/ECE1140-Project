"""
	UNIT Testing for SWTrain Controller File

	Author: Collin Hough

	Date: 18 November 2020
"""
import sys
sys.path.append(".")
from src.SWTrainController.Controller import Controller

def test_default_constructor():
    """ Test creation of new singleton controller """
    test_obj = Controller()
	# Use getPowerCommand method to test creation of default object
    assert test_obj.power_command == 0

def test_initialized_constructor():
    """ Test initialized constructor and set Kp """
    # Create new controller with initialized command speed, current speed, and authority
    test_obj = Controller(3,4,1)

    # Test initialized controller by checking value of command speed
    assert test_obj.command_speed == 3
    assert test_obj.current_speed == 4
    assert test_obj.authority == 1

def test_calculate_power():
    """ Test calculatePower """
    # Create new controller
    test_obj = Controller(40,0,1)

    # Set Kp and Ki
    test_obj.kp = 3
    test_obj.ki = 2
    
    # Turn service brake off
    test_obj.service_brake = False

    # Calculate power
    test_obj.calculate_power()
    assert round(test_obj.power_command, 2) == 35.56
    
    # Input a new command speed and recalculate power
    test_obj.current_speed = 10
    assert round(test_obj.power_command, 2) == 35.56
    test_obj.calculate_power()
    assert round(test_obj.power_command, 2) == 25.69

def test_toggle_mode():
    """ Test changing mode """
    # Create new controller
    test_obj = Controller()
    # Attempt changing mode
    test_obj.toggle_mode("OvErRiDe")
    assert test_obj.mode == 0
    # Correctly change mode
    test_obj.toggle_mode("override")
    assert test_obj.mode == 1

def test_toggle_doors():
    """ Test door toggle """
    # Create new controller
    test_obj = Controller()
    # Open doors
    test_obj.toggle_doors()
    assert test_obj.doors == 1
    # Close doors
    test_obj.toggle_doors()
    assert test_obj.doors == 0
    # Open doors one more time
    test_obj.toggle_doors()
    assert test_obj.doors == 1

def test_toggle_lights():
    """ Test light toggle """
    # Create new controller
    test_obj = Controller()
    # Turn lights on
    test_obj.toggle_lights()
    assert test_obj.lights == 1
    # Turn lights off
    test_obj.toggle_lights()
    assert test_obj.lights == 0
    # Turn lights on one more time
    test_obj.toggle_lights()
    assert test_obj.lights == 1

def test_announce_stations():
    """ Test station announcements """
    # Create new controller
    test_obj = Controller()
    # Turn announcements on
    test_obj.toggle_announcements()
    assert test_obj.announcements == 1
    # Turn announcements off
    test_obj.toggle_announcements()
    assert test_obj.announcements == 0
    # Turn announcements on one more time
    test_obj.toggle_announcements()
    assert test_obj.announcements == 1

def test_advertisements():
    """ Test advertisements toggle """
    # Create new controller
    test_obj = Controller()
    # Turn advertisements on
    test_obj.toggle_ads()
    assert test_obj.advertisements == 1
    # Turn advertisements off
    test_obj.toggle_ads()
    assert test_obj.advertisements == 0
    # Turn advertisements on one more time
    test_obj.toggle_ads()
    assert test_obj.advertisements == 1
