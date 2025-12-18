# demo_module/utils.py
"""Small demo utilities."""

def compute_area(width, height):
    if width is None or height is None:
        raise TypeError("width and height must be numbers")
    try:
        if width < 0 or height < 0:
            raise ValueError("dimensions must be non-negative")
    except TypeError:
        raise TypeError("width and height must be numbers")
    return width * height

def parse_profile_string(s):
    if not isinstance(s, str):
        raise TypeError("profile must be a string")
    try:
        t = s[0]
        rest = s[1:]
        a_str, b_str = rest.split('x')
        return {"type": t, "a": int(a_str), "b": int(b_str)}
    except:
        raise ValueError("invalid profile format")
