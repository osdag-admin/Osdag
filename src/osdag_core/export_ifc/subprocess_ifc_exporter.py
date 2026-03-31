import sys
import json
import os
import argparse
from types import SimpleNamespace

# Make sure we can import osdag_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from osdag_core.export_ifc.ifc_generator import OsdagIfcExporter

class DictToObj(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, DictToObj(value))
            elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                setattr(self, key, [DictToObj(v) for v in value])
            else:
                setattr(self, key, value)
    
    @property
    def __class__(self):
        # We need this to fake the class name for geometry_mapper
        class FakeClass:
            __name__ = getattr(self, '_class_name', 'Unknown')
        return FakeClass

def run_export(json_path, ifc_path, connection_id):
    print(f"[Subprocess] Loading JSON data from {json_path}")
    with open(json_path, 'r') as f:
        data = json.load(f)
        
    members = [DictToObj(m) for m in data.get('members', [])]
    plates = [DictToObj(p) for p in data.get('plates', [])]
    bolts = [DictToObj(b) for b in data.get('bolts', [])]
    welds = [DictToObj(w) for w in data.get('welds', [])]
    others = [DictToObj(o) for o in data.get('others', [])]
    metadata = data.get('metadata', {})
    
    print(f"[Subprocess] Metadata payload received: {metadata}")
    
    print(f"[Subprocess] Exporting to IFC: {ifc_path}")
    exporter = OsdagIfcExporter(filename=ifc_path)
    exporter.export_connection(
        connection_id=connection_id,
        members=members,
        plates=plates,
        bolts=bolts,
        welds=welds if welds else None,
        others=others if others else None,
        metadata=metadata
    )
    exporter.save()
    print(f"[Subprocess] IFC Success.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export serialized OSDAG CAD objects to IFC via subprocess")
    parser.add_argument("--json", required=True, help="Input serialized JSON file")
    parser.add_argument("--ifc", required=True, help="Output IFC file path")
    parser.add_argument("--id", required=True, help="Connection ID")
    
    args = parser.parse_args()
    
    try:
        run_export(args.json, args.ifc, args.id)
        sys.exit(0)
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)
