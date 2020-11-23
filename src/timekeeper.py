"""Module for keeping time of the system"""

import threading
import time

from src.signals import signals
from src.logger import get_logger

logger = get_logger(__name__)

# pylint: disable=too-many-instance-attributes
class Timekeeper:
    """Class responsible for keeping the system time"""
    def __init__(self):
        self.timer_thread = threading.Thread(target=self.timer_function)
        self.signal_period = 0.1
        self.time_factor = 1
        self.current_time_sec = 0
        self.current_time_min = 0
        self.current_time_hour = 1
        self.current_day = 0
        self.run_lock = threading.Lock()
        self.running = True

        self.signal_timer = threading.Timer(self.signal_period * self.time_factor,
                                            self.signal_timer_triggered)
        self.signal_timer.start()

        signals.swtrain_time_trigger.connect(lambda: print("Timer triggered"))

        # For CTC to store trains to be dispatched
        self.ctc_trains_backlog = []

    def signal_timer_triggered(self):
        """Method called when the signal timer thread ends"""
        signals.swtrain_time_trigger.emit()

        self.signal_timer = threading.Timer(self.signal_period * self.time_factor,
                                            self.signal_timer_triggered)

        with self.run_lock:
            self.signal_timer.start()

    def timer_function(self):
        """Thread function for monitoring time and emitting signals"""
        logger.critical("Timekeeper starting...")
        while self.running:
            time.sleep(self.time_factor)

            with self.run_lock:
                self.current_time_sec += 1
                if self.current_time_sec == 60:
                    self.current_time_sec = 0
                    self.current_time_min += 1

                if self.current_time_min == 60:
                    self.current_time_min = 0
                    self.current_time_hour += 1

                if self.current_time_hour == 24:
                    self.current_time_hour = 1
                    self.current_day = (self.current_day + 1) % 6

                signals.timer_expired.emit(self.current_day,
                                           self.current_time_hour,
                                           self.current_time_min,
                                           self.current_time_sec)

                # Dispatch train if needed
                for item in self.ctc_trains_backlog:
                    if (item.hour == self.current_time_hour) and \
                       (item.min == self.current_time_min):
                        signals.dispatch_scheduled_train.emit(item.destination_block, item.line_on)
                        # Remove the train from backlog if dispatched
                        self.ctc_trains_backlog.remove(item)

        # Cancel the timer
        self.signal_timer.cancel()

    def start_time(self):
        """Initially starts the thread"""
        self.timer_thread.start()

    def pause_time(self):
        """Acquires the run lock, so the timer can't run"""
        if not self.run_lock.locked():
            self.run_lock.acquire()

    def resume_time(self):
        """Releases the run lock, so the timer can continue"""
        if self.run_lock.locked():
            self.run_lock.release()

timekeeper = Timekeeper()
