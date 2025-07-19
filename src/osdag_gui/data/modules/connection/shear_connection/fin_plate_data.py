import sqlite3
from osdag_gui.data.database.db_manager import DatabaseManager

class Data:
    def __init__(self):
        db_manager = DatabaseManager()
        conn = db_manager.conn 
        # This line is crucial to get dictionary-like results
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Columns")
        rows = cursor.fetchall()
        column_sections = [row['Designation'] for row in rows]

        cursor.execute("SELECT * FROM Beams")
        beam = cursor.fetchall()
        primary_beams = [row['Designation'] for row in beam]
        secondary_beams = [row['Designation'] for row in beam]

        cursor.execute("SELECT * FROM Material")
        Mat = cursor.fetchall()
        materials = [row['Grade'] for row in Mat]
        
        # The rest of your function remains exactly the same...
        self.connectivity_configs = {
            
        }
        self.connectivity_configs = {
            "Connectivity *": {
                "Column Flange-Beam Web": {
                    "image": ":/images/colF2.png",
                    "fields": [
                        {"label": "Column Section *", "items": column_sections},
                        {"label": "Primary Beam *", "items": primary_beams},
                        {"label": "Material *", "items": materials}
                    ]
                },
                "Column Web-Beam Web": {
                    "image": ":/images/colW1.png",
                    "fields": [
                        {"label": "Column Section *", "items": column_sections},
                        {"label": "Primary Beam *", "items": primary_beams},
                        {"label": "Material *", "items": materials}
                    ]
                },
                "Beam-Beam": {
                    "image": ":/images/fin_beam_beam.png",
                    "fields": [
                        {"label": "Primary Beam *", "items": primary_beams},
                        {"label": "Secondary Beam *", "items": secondary_beams},
                        {"label": "Material *", "items": materials}
                    ]
                }
            }
        }
        self.group_configs = {
            "Factored Loads": {
                "fields": [
                    {"label": "Shear Force (kN)", "placeholder": "ex. 10 kN"},
                    {"label": "Axial Force (kN)", "placeholder": "ex. 10 kN"}
                ]
            },
            "Bolt": {
                "fields": [
                    {"label": "Diameter (mm) *", "items": ["All", "Customized"]},
                    {"label": "Type *", "items": ["Bearing Bolt", "Friction Grip Bolt"]},
                    {"label": "Property Class *(mm)", "items": ["All", "Customized"]}
                ]
            },
            "Plate": {
                "fields": [
                    {"label": "Thickness (mm) *", "items": ["All", "Customized"]}
                ]
            }
        }
        self.make_label_size_equal()

    def make_label_size_equal(self):
        # Collect all label strings from connectivity_configs and group_configs
        labels = []
        for label in self.connectivity_configs.keys():
            labels.append(label)
            label_dict = self.connectivity_configs[label]
            for config in label_dict.values():
                for field in config['fields']:
                    labels.append(field['label'])
        for config in self.group_configs.values():
            for field in config['fields']:
                labels.append(field['label'])
        # Find max length
        max_len = max(len(label) for label in labels)
        # Pad all labels to max_len
        for label in self.connectivity_configs.keys():
            for config in label_dict.values():
                for field in config['fields']:
                    field['label'] = field['label'].ljust(max_len)

        label = list(self.connectivity_configs.keys())[0]
        self.connectivity_configs[label.ljust(max_len)] = self.connectivity_configs[label]
        del self.connectivity_configs[label]

        for config in self.group_configs.values():
            for field in config['fields']:
                field['label'] = field['label'].ljust(max_len)