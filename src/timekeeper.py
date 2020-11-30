"""Module for keeping time of the system"""

import threading
import time

from src.signals import signals
from src.logger import get_logger
from src.CTC.train_system import ctc
from src.common_def import Line

logger = get_logger(__name__)

# pylint: disable=too-many-instance-attributes
class Timekeeper:
    """Class responsible for keeping the system time"""
    def __init__(self):
        self.timer_thread = threading.Thread(target=self.timer_function)
        self.signal_period = 0.2
        self.time_factor = 1
        self.current_time_sec = 0
        self.current_time_min = 0
        self.current_time_hour = 24
        self.current_day = 0
        self.run_lock = threading.Lock()
        self.running = True
        self.paused = False

        self.signal_timer = threading.Timer(self.signal_period * self.time_factor,
                                            self.signal_timer_triggered)

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

                if (self.current_time_hour == 24) and \
                   (self.current_time_min == 0) and \
                   (self.current_time_sec == 0):
                    self.current_day = (self.current_day + 1) % 6

                if self.current_time_hour == 25:
                    self.current_time_hour = 1

                signals.timer_expired.emit(self.current_day,
                                           self.current_time_hour,
                                           self.current_time_min,
                                           self.current_time_sec)

                # Dispatch train if needed
                for item in self.ctc_trains_backlog:
                    if item.hour == self.current_time_hour and \
                    item.min == self.current_time_min:

                        # Check that dispatch to blocks are clear
                        allowed = True
                        if item.line_on == Line.LINE_GREEN:
                            if ctc.blocks_red_arr[61].occupied:
                                logger.critical('CTC : Scheduled Train Delayed ... 1min')

                                item.min += 1
                                if item.min == 60:
                                    item.min = 0
                                    item.hour += 1
                                if item.hour == 24:
                                    item.hour = 0

                                allowed = False
                            else:
                                for i in range(len(ctc.trains_arr)):
                                    if ctc.trains_arr[i].line_on == Line.LINE_GREEN and\
                                    ctc.trains_arr[i].index_on_route == 0:
                                        logger.critical('CTC : Scheduled Train Delayed ... 1min')

                                        item.min += 1
                                        if item.min == 60:
                                            item.min = 0
                                            item.hour += 1
                                        if item.hour == 24:
                                            item.hour = 0

                                        allowed = False
                                        break

                        # For Red Line
                        else:
                            if ctc.blocks_red_arr[8].occupied:
                                logger.critical('CTC : Scheduled Train Delayed ... 1min')

                                item.min += 1
                                if item.min == 60:
                                    item.min = 0
                                    item.hour += 1
                                if item.hour == 24:
                                    item.hour = 0

                                allowed = False
                            else:
                                for i in range(len(ctc.trains_arr)):
                                    if ctc.trains_arr[i].line_on == Line.LINE_RED and\
                                    ctc.trains_arr[i].index_on_route == 0:
                                        logger.critical('CTC : Scheduled Train Delayed ... 1min')

                                        item.min += 1
                                        if item.min == 60:
                                            item.min = 0
                                            item.hour += 1
                                        if item.hour == 24:
                                            item.hour = 0

                                        allowed = False
                                        break

                        if not allowed:
                            continue

                        signals.dispatch_scheduled_train.emit(item.destination_block, item.line_on)
                        # Remove the train from backlog if dispatched
                        self.ctc_trains_backlog.remove(item)

                # Send signal to Track Model if time is right
                if (self.current_time_sec == 5) and \
                   (self.current_time_min == 0) and \
                   (self.current_time_hour == 24):
                    signals.trackmodel_update_tickets_sold.emit()

        # Cancel the timer
        self.signal_timer.join()
        self.signal_timer.cancel()

    def start_time(self):
        """Initially starts the thread"""
        self.timer_thread.start()
        self.signal_timer.start()

    def stop_time(self):
        """Stops the timekeeper"""
        self.running = False
        self.resume_time()
        self.timer_thread.join()

    def pause_time(self):
        """Acquires the run lock, so the timer can't run"""
        if not self.run_lock.locked():
            self.run_lock.acquire()
            self.paused = True

    def resume_time(self):
        """Releases the run lock, so the timer can continue"""
        if self.run_lock.locked():
            self.run_lock.release()
            self.paused = False

timekeeper = Timekeeper()
