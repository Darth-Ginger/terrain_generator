import inspect
import os
import sys
from typing import Any, Dict, Type
from abc import ABC, abstractmethod
import importlib


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
        Discover all subclasses of GenericMap.

        Returns:
            Dict[str, Type[GenericMap]]: A dictionary mapping class names to their class objects.
        """
        current_dir = os.path.dirname(__file__)
        map_classes = {}
       
        
        for filename in os.listdir(current_dir):
            if filename.endswith("_map.py") and filename != os.path.basename(__file__):
                filename = filename[:-3]  # Remove .py extension
                module_name = f"{filename}"  # Remove .py extension
                module = importlib.import_module(module_name)
                class_name = "".join(word.capitalize() for word in filename.split('_'))
                subclass = getattr(module, class_name)
                # issubclass(GenericMap, module_name)
                print(f"{module_name}: {issubclass(subclass, getattr(importlib.import_module('generic_map'), 'GenericMap').__class__)}")
        return {
            subclass.__name__: subclass
            for subclass in cls.__subclasses__()
        }
        

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
        
        
if __name__ == "__main__":
    map_classes = GenericMap.discover_map_classes()
    print(map_classes)