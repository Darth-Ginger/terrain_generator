def dict_to_str(d: dict) -> str:
        """Converts a dictionary to a string, handling np.floats."""
        return "{\n  " + ",\n  ".join(f'"{k}": {v if isinstance(v, str) else str(v)}' for k, v in d.items()) + "\n}"