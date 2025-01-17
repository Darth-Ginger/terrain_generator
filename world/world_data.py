from typing import Any, Dict, Optional
from dataclasses import dataclass, field
import json
from maps.generic_map import GenericMap

@dataclass
class WorldData:
    """
    A data class to store world data and metadata.
    
    Attributes:
        meta_data (Dict[str, Any]): Dictionary storing all metadata.
        maps (Dict[str, GenericMap]): Dictionary of map objects.
    """
    meta_data: Dict[str, Any] = field(default_factory=dict)
    maps: Dict[str, GenericMap] = field(default_factory=dict)

    #region Properties
    @property
    def width(self) -> int:
        return self.meta_data.get("width", 0)

    @width.setter
    def width(self, value: int):
        self.meta_data["width"] = value

    @property
    def height(self) -> int:
        return self.meta_data.get("height", 0)

    @height.setter
    def height(self, value: int):
        self.meta_data["height"] = value

    @property
    def seed(self) -> Optional[int]:
        return self.meta_data.get("seed")

    @seed.setter
    def seed(self, value: Optional[int]):
        self.meta_data["seed"] = value

    #endregion Properties
    
    def add_map(self, name: str, map_object: GenericMap):
        """Add a map to the maps dictionary."""
        self.maps[name] = map_object

    def get_map(self, name: str) -> Optional[GenericMap]:
        """Retrieve a map by its name."""
        return self.maps.get(name)

    def to_json(self, filename: str):
        """Serialize the WorldData to a JSON file."""
        data = {
            "meta_data": self.meta_data,
            "maps": {map_name: map_obj.to_dict() for map_name, map_obj in self.maps.items()}
        }
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    @classmethod
    def from_json(cls, filename: str) -> "WorldData":
        """Deserialize WorldData from a JSON file."""
        with open(filename, "r") as file:
            data = json.load(file)
        instance = cls(meta_data=data["meta_data"])
        for name, map_data in data["maps"].items():
            map_obj = GenericMap.from_type(map_data["type"])
            map_obj.from_dict(map_data)
            instance.add_map(name, map_obj)
        return instance
