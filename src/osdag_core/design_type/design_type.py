class DesignType(object):

    def __init__(self, input_object, design_preferences):
        self.input_object = input_object
        self.output_object = None
        self.design_preferences = design_preferences

    def design(self, calculator):
        self.output_object = calculator.calculate(self.input_object, self.output_object)

