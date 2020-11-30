"""Test for passing track heater"""

from src.SWTrackController.track_system import track_system
from src.signals import signals
from src.common_def import Line

def test_track_heater_green(upload_tracks, download_programs):
    """Turns the track heater on from the track model and ensures that
    the track controllers receive it
    """
    signals.swtrack_set_track_heater.emit(Line.LINE_GREEN, True)

    for track_controller in track_system.green_track_controllers:
        assert track_controller.get_track_heater_status()

    signals.swtrack_set_track_heater.emit(Line.LINE_GREEN, False)

    for track_controller in track_system.green_track_controllers:
        assert not track_controller.get_track_heater_status()
