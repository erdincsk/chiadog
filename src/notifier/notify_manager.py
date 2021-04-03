# std
import logging
from typing import List

# project
from . import Event
from .keep_alive_monitor import KeepAliveMonitor
from .pushover_notifier import PushoverNotifier


class NotifyManager:
    """This class manages all notifiers and propagates
    events to all of them such that notifications can be
    delivered to multiple services at once.
    """

    def __init__(self, config: dict, keep_alive_monitor: KeepAliveMonitor = None):
        self._keep_alive_monitor = keep_alive_monitor or KeepAliveMonitor()
        self._keep_alive_monitor.set_notify_manager(self)
        self._notifiers = []
        self._config = config
        self._initialize_notifiers()

    def _initialize_notifiers(self):
        key_notifier_mapping = {
            "pushover": PushoverNotifier
        }
        for key in self._config.keys():
            if key not in key_notifier_mapping.keys():
                logging.warning(f"Cannot find mapping for {key} notifier.")
            if self._config[key]["enable"]:
                self._notifiers.append(key_notifier_mapping[key](self._config[key]))

    def process_events(self, events: List[Event]):
        """Process all keep-alive and user events"""
        self._keep_alive_monitor.process_events(events)
        for notifier in self._notifiers:
            notifier.send_events_to_user(events)
