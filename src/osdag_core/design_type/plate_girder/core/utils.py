import math

def ceil_to_nearest(x, multiple):
    return float(math.ceil(x / multiple) * multiple)

def get_K_from_warping_restraint(warping_condition):
    """
    Return effective length factor K based on exact warping restraint description (IS 800:2007, Clause E.1).
    """
    if warping_condition == "Both flanges fully restrained":
        return 0.5
    elif warping_condition == "Compression flange fully restrained":
        return 0.7
    elif warping_condition == "Compression flange partially restrained":
        return 0.85
    elif warping_condition == "Warping not restrained in both flanges":
        return 1.0
    else:
        raise ValueError("Invalid warping restraint. Use one of the four standard conditions.")
