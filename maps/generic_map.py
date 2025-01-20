import inspect
import os
import sys
from typing import Any, Dict, Type
from abc import ABC, abstractmethod
import importlib
from maps import *


class GenericMap(ABC):
    """
    Abstract base class for maps.
    Defines the interface for map storage and operations.
    """
    map_type = "GenericMap"
    
    @abstractmethod
    def __init__(self, **kwargs) -> None:
        """
        Initialize the map with dynamic parameters
        """
        pass
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Serialize the map to a dictionary."""
        pass

    @abstractmethod
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Deserialize the map from a dictionary."""
        pass

    @abstractmethod
    def get_data(self, *args, **kwargs) -> Any:
        """Retrieve data from the map."""
        pass
        
if __name__ == "__main__":
    map_classes = GenericMap.discover_map_classes()
    print(map_classes)