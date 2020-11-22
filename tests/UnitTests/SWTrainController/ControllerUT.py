"""
	UNIT Testing for SWTrain Controller File

	Author: Collin Hough

	Date: 18 November 2020
"""
import sys
sys.path.insert(1, '../../..')
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

    # Calculate power
    test_obj.calculate_power()
    assert test_obj.power_command == 130

    # Input a new command speed and recalculate power
    test_obj.current_speed = 10
    assert test_obj.power_command == 130
    test_obj.calculate_power()
    assert test_obj.power_command == 117.5

def test_toggle_mode():
    """ Test changing mode """
    # Create new controller
    test_obj = Controller()
    # Attempt changing mode
    assert test_obj.toggle_mode("OvErRiDe") == 0
    # Correctly change mode
    assert test_obj.toggle_mode("override") == 1

def test_toggle_doors():
    """ Test door toggle """
    # Create new controller
    test_obj = Controller()
    # Open doors
    assert test_obj.toggleDoors() == 1
    # Close doors
    assert test_obj.toggleDoors() == 0
    # Open doors one more time
    assert test_obj.toggleDoors() == 1

def test_toggle_lights():
    """ Test light toggle """
    # Create new controller
    test_obj = Controller()
    # Turn lights on
    assert test_obj.toggleLights() == 1
    # Turn lights off
    assert test_obj.toggleLights() == 0
    # Turn lights on one more time
    assert test_obj.toggleLights() == 1

def test_announce_stations():
    """ Test station announcements """
    # Create new controller
    test_obj = Controller()
    # Turn announcements on
    assert test_obj.announceStations() == 1
    # Turn announcements off
    assert test_obj.announceStations() == 0
    # Turn announcements on one more time
    assert test_obj.announceStations() == 1

def test_advertisements():
    """ Test advertisements toggle """
    # Create new controller
    test_obj = Controller()
    # Turn advertisements on
    assert test_obj.toggleAds() == 1
    # Turn advertisements off
    assert test_obj.toggleAds() == 0
    # Turn advertisements on one more time
    assert test_obj.toggleAds() == 1
