def sort_dict(d: dict, ascending: bool = False) -> dict:
    """
    Sort a dictionary by its values.
    """
    return {k: v for k, v in sorted(d.items(), key=lambda x: x[1], reverse=not ascending)}
