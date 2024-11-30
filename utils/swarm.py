import logging
from typing import Callable, Dict, List

logger = logging.getLogger(__name__)

class Swarm:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
        logger.debug(f"Handler subscribed to event '{event_type}'.")

    def publish(self, event_type: str, data):
        handlers = self.subscribers.get(event_type, [])
        logger.debug(f"Publishing event '{event_type}' to {len(handlers)} handler(s).")
        for handler in handlers:
            handler(data)

# Singleton instance of Swarm
swarm = Swarm() 