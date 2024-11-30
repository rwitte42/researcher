import logging
from typing import Callable, Dict, List

logger = logging.getLogger(__name__)

class Swarm:
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls):
        if cls._instance is None:
            logger.debug("Creating new Swarm singleton instance.")
            cls._instance = super(Swarm, cls).__new__(cls)
            # Initialization of instance variables will be handled in __init__
        else:
            logger.debug("Swarm singleton instance already exists.")
        return cls._instance

    def __init__(self):
        # Initialize subscribers only once
        if not hasattr(self, 'subscribers'):
            self.subscribers: Dict[str, List[Callable]] = {}
            logger.debug("Initializing Swarm subscribers.")

    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        else:
            if handler in self.subscribers[event_type]:
                logger.warning(f"Handler '{handler.__name__}' is already subscribed to event '{event_type}'.")
                return
            
        self.subscribers[event_type].append(handler)
        logger.debug(f"Handler '{handler.__name__}' subscribed to event '{event_type}'.")

    def publish(self, event_type: str, data):
        handlers = self.subscribers.get(event_type, [])
        logger.debug(f"Publishing event '{event_type}' to {len(handlers)} handler(s).")
        for handler in handlers:
            handler(data)

# Singleton instance of Swarm
swarm = Swarm()