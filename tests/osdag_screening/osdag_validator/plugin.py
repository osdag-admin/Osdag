from .core import (
    Validator,
    ConnectionValidator,
    ShearConnectionValidator,
    FinPlateConnectionValidator,
    EndPlateConnectionValidator,
)

def load_plugin():
    return {
        "validator": Validator,
        "connection_validator": ConnectionValidator,
        "shear_validator": ShearConnectionValidator,
        "fin_plate_validator": FinPlateConnectionValidator,
        "end_plate_validator": EndPlateConnectionValidator,
    }
