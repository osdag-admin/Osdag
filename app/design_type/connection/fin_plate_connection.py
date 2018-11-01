from app.design_type.connection.shear_connection import ShearConnection
from app.Utils.Common.FinPlateInputObject import FinPlateInputObject
from app.Utils.Common.FinPlateOutputObject import FinPlateOutputObject
import app.Utils.Calculations.FinPlateCalculator as FinPlateCalculator

class FinPlateConnection (ShearConnection):
    input_object = FinPlateInputObject()
    output_object = FinPlateOutputObject()

    def design(self):
        self.output_object = FinPlateCalculator.calculate(self.input_object, self.design_preferences)

if __name__ == "__main__":
    fpc = FinPlateConnection()
    fpio = FinPlateInputObject()
    fpoo = FinPlateOutputObject()
    fpc.input_object = fpio
    fpc.output_object = fpoo
    print(fpio.a)
    print(fpc.output_object.c)
    fpc.design()
    print(fpc.output_object.c)

