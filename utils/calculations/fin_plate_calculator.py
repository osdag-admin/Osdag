from app.utils.common.fin_plate_output import FinPlateOutputObject


def calculate(input_object, design_preferences):
    a = input_object.a
    b = input_object.b

    fpoo = FinPlateOutputObject()
    fpoo.c = a + b

    return fpoo