
from typing import Tuple

# Grid settings
GRID_SIZE: Tuple[int, int] = (5, 5)  # X and Y dimensions
MAX_ELEVATION: float = 10.0  # Max elevation in kilometers
MAX_DEPTH: float = 5.0  # Max depth in kilometers
SEED: int = 42  # Random seed for reproducibility

# Noise settings
PERLIN_SCALE: float = 0.1
VORONOI_REGIONS: int = 50

# Erosion settings
EROSION_ITERATIONS: int = 5
        