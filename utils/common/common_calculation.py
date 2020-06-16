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


def choose_higher_value(min_value, available_values):
    """Choose a smallest value, higher than or equal to min_value from the list of available values

    :param min_value: float
    :param available_values: list
    :return: float
    # TODO: What if the min_value is higher than all values in the list
    # TODO: if min_value is higher it will return None which should be checked where fuction is called
    # TODO: write min() only if filter returns some value. else it will throw error: 'min() arg is an empty sequence'
    """
    return min(filter(lambda i: i >= min_value, available_values))


def choose_smaller_value(max_value, available_values):
    """Choose a highest value, smaller than or equal to min_value from the list of available values

    :param max_value: float
    :param available_values: list
    :return: float
    # TODO: What if the max_value is smaller than all values in the list
    """
    return max(filter(lambda i: i <= max_value, available_values))


def choose_next_value(current_value, available_values):
    """Choose next value, higher than current_value from the list of available values

    :param current_value: float
    :param available_values: list
    :return: float
    # TODO: What if the current_value is higher than all values in the list
    """
    return min(filter(lambda i: i > current_value, available_values))


def choose_previous_value(current_value, available_values):
    """Choose the previous value, smaller than current_value from the list of available values

    :param current_value: float
    :param available_values: list
    :return: float
    # TODO: What if the current_value is smaller than all values in the list
    """
    return max(filter(lambda i: i <= current_value, available_values))


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

