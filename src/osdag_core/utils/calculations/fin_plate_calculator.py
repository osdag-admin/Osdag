from ..common.output import FinPlateConnectionOutput


def calculate(input_object, design_preferences):
    a = input_object.a
    b = input_object.b

    fpoo = FinPlateConnectionOutput()
    fpoo.c = a + b

    return fpoo
