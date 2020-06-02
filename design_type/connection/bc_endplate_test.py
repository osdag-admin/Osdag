import yaml
from design_type.connection.beam_column_end_plate import BeamColumnEndPlate


# Load osi file
# Get input objects
input_file_path = "/home/ajmalbabums/Desktop/OsdagWorkspace/bcinput.osi"
design_dictionary = yaml.load(input_file_path, Loader=yaml.FullLoader)