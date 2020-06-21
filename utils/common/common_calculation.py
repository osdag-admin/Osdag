import math
import numpy as np


class Value(object):
    def __init__(self, provided=0.0, min=0.0, max=0.0, available_values=None):
        self.available_values = available_values
        self.min = min
        self.max = max
        self.provided = provided


def round_up(value, multiplier=1, minimum_value=0):
    """Round up the value to the next multiple of 'multiplier' with a minimum of 'minimum_value'"""
    value = max(value, minimum_value)
    return math.ceil(value / multiplier) * multiplier


def round_down(value, multiplier=1, minimum_value=0):
    """Round up the value to the next multiple of 'multiplier' with a minimum of 'minimum_value'"""
    value = max(value, minimum_value)
    return math.floor(value / multiplier) * multiplier


def choose_higher_value(min_value, available_values, max_value=None):
    """Choose a smallest value, higher than or equal to min_value from the list of available values

    :param min_value: float
    :param available_values: list
    :param max_value: Maximum value can take - optional
    :return: float
    NOTE: if the min_value is higher than all values in the list, returns None
    """
    try:
        if max_value is not None:
            available_values = list([x for x in available_values if (x <= max_value)])
        return min(filter(lambda i: i >= min_value, available_values))
    except ValueError:
        return None


def choose_smaller_value(max_value, available_values, min_value=None):
    """Choose a highest value, smaller than or equal to min_value from the list of available values

    :param max_value: float
    :param available_values: list
    :param min_value: Minimum value can take - optional
    :return: float
    Note: if the max_value is smaller than all values in the list, returns None
    """
    try:
        if min_value is not None:
            available_values = list([x for x in available_values if (x >= min_value)])
        return max(filter(lambda i: i <= max_value, available_values))
    except ValueError:
        return None


def choose_next_value(current_value, available_values, max_value=None):
    """Choose next value, higher than current_value from the list of available values

    :param current_value: float
    :param available_values: list
    :param max_value: Maximum value can take - optional
    :return: next possible value - float
    Note: if the current_value is higher than all values in the list, returns None
    """

    try:
        if max_value is not None:
            available_values = list([x for x in available_values if (x <= max_value)])
        return min(filter(lambda i: i > current_value, available_values))
    except ValueError:
        return None


def choose_previous_value(current_value, available_values, min_value=None):
    """Choose the previous value, smaller than current_value from the list of available values

    :param current_value: float
    :param available_values: list
    :param min_value: Minimum value can take - optional
    :return: previous possible value - float
    Note: if the current_value is smaller than all values in the list, returns None
    """

    try:
        if min_value is not None:
            available_values = list([x for x in available_values if (x >= min_value)])
        return max(filter(lambda i: i < current_value, available_values))
    except ValueError:
        return None


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

