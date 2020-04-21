import math
import numpy as np


def round_up(value, multiplier=1, minimum_value=0):
    """Round up the value to the next multiple of 'multiplier' with a minimum of 'minimum_value'"""
    value = max(value, minimum_value)
    return math.ceil(value / multiplier) * multiplier


def round_down(value, multiplier=1, minimum_value=0):
    """Round up the value to the next multiple of 'multiplier' with a minimum of 'minimum_value'"""
    value = max(value, minimum_value)
    return math.floor(value / multiplier) * multiplier


def calculate_roots(lst=None):
    """Calculate the roots for a given equation

    Args: list (list): a list with the values of the constants

    Returns: highest positive (real) value
    """
    if lst is None:
        lst = []
    else:
        lst = lst

    roots = np.roots(lst)  # finding roots of the equation
    r_1 = roots[0]
    r_2 = roots[1]
    r = max(r_1, r_2)  # picking the highest positive value from the roots

