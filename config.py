
from typing import Tuple

# Logging settings
LOGGING_LEVEL = "DEBUG"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
ENABLE_TERMINAL_LOGGING = True  # Enable/disable terminal logging
ENABLE_FILE_LOGGING = True  # Enable/disable file logging
VERBOSE_LOGGING = False  # Enable/disable verbose logging
LOG_FILE_PATH = "logs/app.log"  # Path for the log file
DEBUG_OUTPUT_FILE = "logs/debug_output.log"  # Path for debug output


# Grid settings
GRID_SIZE: Tuple[int, int] = (500, 500)  # X and Y dimensions
MAX_ELEVATION: float = 5.0  # Max elevation in kilometers
MAX_DEPTH: float = 1.0  # Max depth in kilometers
SEED: int = 42  # Random seed for reproducibility

# Noise settings
PERLIN_SCALE: float = 0.1
VORONOI_REGIONS: int = 10

# Erosion settings
EROSION_ITERATIONS: int = 5
        