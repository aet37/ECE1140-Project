"""Module for keeping time of the system"""

import threading
import time

from src.signals import signals

class Timekeeper:
    """Class responsible for keeping the system time"""
    def __init__(self):
        self.timer_thread = threading.Thread(target=self.timer_function)
        self.timer_period_in_sec = 0.1
        self.current_time_sec = 0
        self.current_time_min = 0
        self.current_time_hour = 0
        self.run_lock = threading.Lock()
        self.running = True

    def timer_function(self):
        """Thread function for monitoring time and emitting signals"""
        while self.running:
            time.sleep(self.timer_period_in_sec)

            with self.run_lock:
                self.current_time_sec += 1
                if self.current_time_sec == 60:
                    self.current_time_sec = 0
                    self.current_time_min += 1

                if self.current_time_min == 60:
                    self.current_time_min = 0
                    self.current_time_hour += 1

                if self.current_time_hour == 24:
                    self.current_time_hour = 0

                signals.timer_expired.emit(self.current_time_hour,
                                           self.current_time_min,
                                           self.current_time_sec)

    def start_time(self):
        """Initially starts the thread"""
        self.timer_thread.start()

    def pause_time(self):
        """Acquires the run lock, so the timer can't run"""
        self.run_lock.acquire()

    def resume_time(self):
        """Releases the run lock, so the timer can continue"""
        self.run_lock.release()

timekeeper = Timekeeper()
