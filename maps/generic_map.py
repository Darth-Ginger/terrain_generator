import inspect
import os
import sys
from typing import Any, Dict, Type
from abc import ABC, abstractmethod
import importlib
import pkgutil

class GenericMap(ABC):
    """
    Abstract base class for maps.
    Defines the interface for map storage and operations.
    """
    
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
    
    @classmethod
    def discover_map_classes(cls) -> Dict[str, Type["GenericMap"]]:
        """
        Discover all subclasses of GenericMap in the current module.
        
        Returns:
            Dict[str, Type[GenericMap]]: A dictionary mapping class names to class objects.
        """
        map_classes = {}
        dir_path = os.path.dirname(os.path.abspath(__file__))
        for filename in os.listdir(dir_path):
            if filename.endswith('_map.py') and filename != 'generic_map.py':
                #TODO Update this to get the module name from the file itself
                module_name = filename[:-3]  # remove .py extension
                module = importlib.import_module(module_name)
                for obj_name, obj in module.__dict__.items():
                    if inspect.isclass(obj) and issubclass(obj, cls) and obj is not cls:
                        map_classes[obj_name] = obj
        return map_classes
        

    @classmethod
    def from_type(cls, map_type: str, **kwargs) -> Type["GenericMap"]:
        """
        Factory method to create a map instance by type.

        Args:
            map_type (str): The name of the map class to create.
            **kwargs: Additional arguments to pass to the map's constructor.

        Returns:
            GenericMap: An instance of the specified map class.

        Raises:
            ValueError: If the specified map_type is not found.
        """
        
        # Discover all subclasses of GenericMap in the current module
        map_classes = cls.discover_map_classes()
        
        # Check if requested map type is available
        if map_type not in map_classes:
            raise ValueError(f"Unknown map type: {map_type}")
        
        # Create an instance of the requested map type
        return map_classes[map_type](**kwargs)
        