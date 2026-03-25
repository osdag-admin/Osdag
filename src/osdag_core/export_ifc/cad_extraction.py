import sys
import re

def assign_ifc_name(cad_obj, attr_name, connection_type=None):
    """
    Translates internal CAD attribute names (e.g., 'plateAbvFlange') 
    into human-readable IFC entity names matching the Osdag GUI.
    Attaches the label to the cad_obj.ifc_name property.
    """
    if str(attr_name).startswith('_'):
        attr_name = attr_name.lstrip('_')
    
    attr_name_lower = attr_name.lower()
    name = "Connection Plate"
    
    # 1. Moment Splice Cover Plates
    if any(x in attr_name_lower for x in ['plateabvflange', 'platebelwflange', 'flangeplate']):
        name = "Flange Plate"
        if "inner" in attr_name_lower:
            name = "Inner Flange Plate"
    elif 'webplate' in attr_name_lower:
        name = "Web Plate"
        
    # 2. Moment End Plates
    elif 'endplate' in attr_name_lower or (connection_type and 'endplate' in connection_type.lower() and attr_name_lower == 'plate'):
        name = "End Plate"
    elif 'contplate' in attr_name_lower:
        name = "Continuity Plate"
    elif 'stiffener' in attr_name_lower or 'stiff_alg' in attr_name_lower:
        name = "Stiffener Plate"
        
    # 3. Base Plates
    elif 'baseplate' in attr_name_lower:
        name = "Base Plate"
    elif 'shearkey' in attr_name_lower:
        name = "Shear Key"
        
    # 4. Shear Connections
    elif 'seatangle' in attr_name_lower or 'topclipangle' in attr_name_lower:
        name = "Seat Angle" if 'seat' in attr_name_lower else "Top Clip Angle"
    elif 'angle' in attr_name_lower:
        name = "Cleat Angle"
    elif connection_type and 'finplate' in connection_type.lower() and attr_name_lower == 'plate':
        name = "Fin Plate"
        
    # 5. Simple Connections & Gussets
    elif 'packing' in attr_name_lower:
        name = "Packing Plate"
    elif 'platec' in attr_name_lower:
        name = "Cover Plate"
    elif attr_name_lower in ['plate1', 'plate2'] and connection_type and ('tension' in connection_type.lower() or 'compression' in connection_type.lower()):
        name = "Gusset Plate"

    # Fallback to Title Case
    if name == "Connection Plate" and attr_name_lower not in ['plate', 'plate1', 'plate2', 'plateleft', 'plateright']:
        # Split CamelCase or snake_case
        words = re.sub(r'([A-Z])', r' \1', attr_name).replace('_', ' ').split()
        if words:
            name = " ".join([w.capitalize() for w in words if not w.lower().endswith('model')])
            if not name.endswith('Plate') and not name.endswith('Angle'):
                name += " Plate"

    cad_obj.ifc_name = name
    return cad_obj

def extract_simple_plated(cad_obj):
    """
    Explicit extractor for Simple Plated connections.
    Handles Bolted/Welded Lap Joints and Bolted/Welded Butt Joints.
    """
    members = []
    plates = []
    bolts = []
    welds = []
    others = []
    
    # Simple joints usually don't have structural 'members' like beams/columns, 
    # but rather just connection plates that act as the members themselves.
    
    # Main Plates
    for attr in ['plate1', 'plate2']:
        if hasattr(cad_obj, attr):
            val = getattr(cad_obj, attr)
            if val is not None:
                plates.append(assign_ifc_name(val, attr, cad_obj.__class__.__name__))
                
    # Splice/Cover Plates (for Bolted Butt Joint)
    # The butt joint has platec and platec2 (bottom cover plate)
    for attr in ['platec', 'platec2']:
        if hasattr(cad_obj, attr):
            val = getattr(cad_obj, attr)
            if val is not None:
                plates.append(assign_ifc_name(val, attr, cad_obj.__class__.__name__))
                
    # Fasteners (for Bolted Lap/Butt joints)
    # The current SimpleConnections directly return separate lists of bolts/nuts instead 
    # of a nut_bolt_array object. We must introspect the tuples returned by the CAD builders 
    # OR assume they will wrap it in an object.
    # Looking at the code, `create_bolted_lap_joint` returns (assembly, p1, p2, bolts, nuts).
    # Since cad_extraction operates on the *OSDAG GUI Module Object* which holds these properties, 
    # we'll look for `bolts` and `nuts` lists directly.
    for attr in ['bolts', 'nuts']:
        if hasattr(cad_obj, attr):
            val = getattr(cad_obj, attr)
            if val is not None and isinstance(val, list):
                bolts.extend(val)

    # Welds (for Welded Lap/Butt joints)
    # Sometimes stored as weld1, weld2, weld_left, weld_right, or in a list `welds`
    if hasattr(cad_obj, 'welds') and isinstance(cad_obj.welds, list):
        welds.extend(cad_obj.welds)
    elif hasattr(cad_obj, 'weld_models') and isinstance(cad_obj.weld_models, list):
        welds.extend(cad_obj.weld_models)
    else:
        for attr in ['weld1', 'weld2', 'weld_left', 'weld_right']:
            if hasattr(cad_obj, attr):
                val = getattr(cad_obj, attr)
                if val is not None:
                    welds.append(val)
                    
    return members, plates, bolts, welds, others

def extract_shear_connections(cad_obj):
    """
    Explicit extractor for Shear Connections.
    Handles Fin Plate, Cleat Angle, End Plate, and Seated Angle variants.
    """
    members = []
    plates = []
    bolts = []
    welds = []
    others = []
    
    # 1. Structural Members
    member_map = [
        ('column', 'columnModel'), ('column', 'column_Model'),
        ('beam', 'beamModel'), ('beam', 'beam_Model'),
        ('supporting', 'supportingModel'), ('supporting', 'columnModel'),
        ('supported', 'supportedModel'), ('supported', 'beamModel'),
        ('supporting', 'supporting_Model'), ('supported', 'supported_Model')
    ]
    for attr, model_attr in member_map:
        if getattr(cad_obj, model_attr, None) is not None:
            val = getattr(cad_obj, attr, None)
            if val is not None and val not in members:
                val.ifc_name = "Column" if 'column' in attr.lower() or 'supporting' in attr.lower() else "Beam"
                members.append(val)
                
    # 2. Connection Plates and Angles
    plate_attrs = ['plate', 'angle', 'angleLeft', 'seatangle', 'topclipangle']
    for attr in plate_attrs:
        # Some use plateModel, some use plate_Model
        model_name = next((attr + m for m in ['Model', '_Model'] if hasattr(cad_obj, attr + m)), None)
        if model_name and getattr(cad_obj, model_name) is not None:
            val = getattr(cad_obj, attr, None)
            if val is not None:
                plates.append(assign_ifc_name(val, attr, cad_obj.__class__.__name__))
                
    # 3. Fasteners (Bolts/Nuts)
    if hasattr(cad_obj, 'nut_bolt_array') and cad_obj.nut_bolt_array is not None:
        nba = cad_obj.nut_bolt_array
        if hasattr(nba, 'bolts'): bolts.extend(nba.bolts)
        if hasattr(nba, 'nuts'): bolts.extend(nba.nuts)
        if hasattr(nba, 'bolts_AF'): bolts.extend(nba.bolts_AF)
        if hasattr(nba, 'nuts_AF'): bolts.extend(nba.nuts_AF)
        
    # 4. Welds (Handling inconsistent weldModelLeft vs weldLeftModel)
    weld_map = [
        ('weldLeft', 'weldModelLeft'), ('weldRight', 'weldModelRight'),
        ('weldLeft', 'weldLeftModel'), ('weldRight', 'weldRightModel'),
        ('weld', 'weldModel'), ('weld', 'weld_Model'),
        ('Fweld1', 'weldModelLeft'), ('Fweld1', 'weldModelRight') # Fallback for some old CADs
    ]
    for attr, model_attr in weld_map:
        if getattr(cad_obj, model_attr, None) is not None:
            val = getattr(cad_obj, attr, None)
            if val is not None and val not in welds:
                welds.append(val)
                
    # Generic scan for safety (excluding already handled and auxiliary ones)
    handled_names = set(plate_attrs) | {'column', 'beam', 'supporting', 'supported', 'weldLeft', 'weldRight', 'weld', 'weldCutPlate'}
    for attr in sorted(dir(cad_obj)):
        if attr.startswith('_') or attr in handled_names: continue
        if attr.endswith('Model') or attr.endswith('_Model'):
            model_val = getattr(cad_obj, attr)
            if model_val is None: continue
            
            base_attr = attr.replace('Model', '').replace('_Model', '')
            # Special case for weldModelLeft -> weldLeft
            if base_attr == 'weld': base_attr = 'weld' # Placeholder
            
            if base_attr in handled_names: continue
            
            val = getattr(cad_obj, base_attr, None)
            if val is not None:
                v_type = type(val).__name__
                if v_type in ('FilletWeld', 'GrooveWeld', 'Weld'):
                    if val not in welds: welds.append(val)
                elif v_type in ('Plate', 'Angle', 'ISection', 'StiffenerPlate'):
                    if v_type == 'Plate' or v_type == 'StiffenerPlate': 
                        if val not in plates: plates.append(assign_ifc_name(val, base_attr, cad_obj.__class__.__name__))
                    elif v_type == 'Angle': 
                        if val not in plates: plates.append(assign_ifc_name(val, base_attr, cad_obj.__class__.__name__))
                    else: 
                        if val not in members: members.append(val)
                
    return members, plates, bolts, welds, others

def extract_base_plate(cad_obj):
    """
    Explicit extractor for Base Plate connections.
    """
    members = []
    plates = []
    bolts = []
    welds = []
    others = []
    
    # 1. Structural Members (Column)
    model_name = next(('column' + m for m in ['Model', '_Model'] if hasattr(cad_obj, 'column' + m)), None)
    if model_name and getattr(cad_obj, model_name) is not None:
        val = getattr(cad_obj, 'column', None)
        if val is not None:
            val.ifc_name = "Column"
            members.append(val)
        
    # 2. Connection Plates & Concrete/Grout
    plate_attrs = [
        'baseplate', 'shearkey_1', 'shearkey_2',
        'stiffener_algflangeL1', 'stiffener_algflangeR1', 'stiffener_algflangeL2', 'stiffener_algflangeR2',
        'stiffener1', 'stiffener2', 'stiffener3', 'stiffener4',
        'stiffener_acrsWeb1', 'stiffener_acrsWeb2',
        'stiffener_insideflange1', 'stiffener_insideflange2',
        'stiff_alg_l1', 'stiff_alg_l2', 'stiff_alg_b1', 'stiff_alg_b2'
    ]
    for attr in plate_attrs:
        model_name = next((attr + m for m in ['Model', '_Model'] if hasattr(cad_obj, attr + m)), None)
        if model_name and getattr(cad_obj, model_name) is not None:
            val = getattr(cad_obj, attr, None)
            if val is not None:
                plates.append(assign_ifc_name(val, attr, cad_obj.__class__.__name__))
                
    # 2b. Concrete & Grout
    for attr in ['concrete', 'grout', 'foundation']:
        model_name = next((attr + m for m in ['Model', '_Model'] if hasattr(cad_obj, attr + m)), None)
        if model_name and getattr(cad_obj, model_name) is not None:
            val = getattr(cad_obj, attr, None)
            if val is not None:
                others.append(val)
                
    # 3. Fasteners (Anchor Bolts/Nuts)
    if hasattr(cad_obj, 'nut_bolt_array') and cad_obj.nut_bolt_array is not None:
        nba = cad_obj.nut_bolt_array
        if hasattr(nba, 'bolts'): bolts.extend(nba.bolts)
        if hasattr(nba, 'nuts'): bolts.extend(nba.nuts)
        
    # 4. Welds (Strict filtering)
    handled_names = set(plate_attrs) | {'column', 'concrete', 'grout', 'foundation', 'weldCutPlate'}
    for attr in sorted(dir(cad_obj)):
        if attr.startswith('_') or attr in handled_names: continue
        if attr.endswith('Model') or attr.endswith('_Model'):
            base_attr = attr.replace('Model', '').replace('_Model', '')
            if base_attr in handled_names: continue
            if getattr(cad_obj, attr) is None: continue
            val = getattr(cad_obj, base_attr, None)
            if val is not None and type(val).__name__ in ('FilletWeld', 'GrooveWeld', 'Weld', 'Weld_sec'):
                welds.append(val)
                
    return members, plates, bolts, welds, others

def extract_moment_endplate(cad_obj):
    """
    Explicit extractor for Moment End Plate connections.
    Handles BC End Plate, BB End Plate splice, and CC End Plate splice.
    """
    members = []
    plates = []
    bolts = []
    welds = []
    others = []
    
    # 1. Structural Members
    member_map = [
        ('column', 'columnModel'), ('column', 'column_Model'),
        ('beam', 'beamModel'), ('beam', 'beam_Model'),
        ('column1', 'column1Model'), ('column1', 'column1_Model'),
        ('column2', 'column2Model'), ('column2', 'column2_Model'),
        ('beamLeft', 'beamLModel'), ('beamRight', 'beamRModel'),
        ('beam1', 'beam1Model'), ('beam1', 'beam1_Model'),
        ('beam2', 'beam2Model'), ('beam2', 'beam2_Model')
    ]
    for attr, model_attr in member_map:
        if getattr(cad_obj, model_attr, None) is not None:
            val = getattr(cad_obj, attr, None)
            if val is not None and val not in members:
                val.ifc_name = "Column" if 'column' in attr.lower() else "Beam"
                members.append(val)
                
    # 2. Plates & Stiffeners
    plate_attrs = [
        'plate', 'plate1', 'plate2', 'plateLeft', 'plateRight', 'endPlate1', 'endPlate2',
        'beam_stiffener_1', 'beam_stiffener_2', 'beam_stiffener_3', 'beam_stiffener_4',
        'beam_stiffener_F1', 'beam_stiffener_F2', 'beam_stiffener_F3', 'beam_stiffener_F4',
        'stiffener1', 'stiffener2',
        'contPlate_L1', 'contPlate_L2', 'contPlate_R1', 'contPlate_R2',
        'webplate_L', 'webplate_R', 'diagplate_L1', 'diagplate_R1'
    ]
    
    # Variant-aware filtering:
    # BBEndplate (Splice): 1,3 = TOP; 2,4 = BOTTOM. Welds 1,3 = TOP; 2,4 = BOTTOM.
    # BCEndplate (Beam-Column): 2 = TOP; 1 = BOTTOM. Welds 1 = TOP; 2 = BOTTOM.
    endplate_type = getattr(cad_obj.module, 'endplate_type', '') if hasattr(cad_obj, 'module') else ''
    is_flushed = "Flushed" in endplate_type
    is_oneway = "Extended One Way" in endplate_type
    is_bc_endplate = hasattr(cad_obj, 'beam') and not hasattr(cad_obj, 'beamLeft')
    
    skipped_attrs = set()
    if is_flushed:
        skipped_attrs = {'beam_stiffener_1', 'beam_stiffener_2', 'beam_stiffener_3', 'beam_stiffener_4'}
    elif is_oneway:
        if is_bc_endplate:
            # BCEndplate: 1 is bottom, 2 is top
            skipped_attrs = {'beam_stiffener_1'}
        else:
            # BBEndplate (Splice): 2,4 are bottom
            skipped_attrs = {'beam_stiffener_2', 'beam_stiffener_4'}

    for attr in plate_attrs:
        if attr in skipped_attrs: continue
        # BBEndplate uses plateLModel and plateRModel instead of plateLeftModel
        model_name = next((attr + m for m in ['Model', '_Model'] if hasattr(cad_obj, attr + m)), None)
        if model_name is None:
            if attr == 'plateLeft': model_name = 'plateLModel' if hasattr(cad_obj, 'plateLModel') else None
            elif attr == 'plateRight': model_name = 'plateRModel' if hasattr(cad_obj, 'plateRModel') else None
            
        if model_name and getattr(cad_obj, model_name) is not None:
            val = getattr(cad_obj, attr, None)
            if val is not None:
                plates.append(assign_ifc_name(val, attr, cad_obj.__class__.__name__))
                
    # 2b. Generic Plate/Stiffener Scan (for missed attributes or variant-specific names)
    handled_names = set(plate_attrs) | set([m[0] for m in member_map]) | {'weldCutPlate'} | skipped_attrs
    for attr in sorted(dir(cad_obj)):
        if attr.startswith('_') or attr in handled_names: continue
        if attr.endswith('Model') or attr.endswith('_Model'):
            base_attr = attr.replace('Model', '').replace('_Model', '')
            if base_attr in handled_names: continue
            if getattr(cad_obj, attr) is None: continue # Skip uninitialized models
            val = getattr(cad_obj, base_attr, None)
            if val is not None and type(val).__name__ in ('Plate', 'StiffenerPlate', 'Stiffener', 'Angle'):
                plates.append(assign_ifc_name(val, base_attr, cad_obj.__class__.__name__))
                
    # 3. Fasteners
    if hasattr(cad_obj, 'nut_bolt_array') and cad_obj.nut_bolt_array is not None:
        nba = cad_obj.nut_bolt_array
        if hasattr(nba, 'bolts'): bolts.extend(nba.bolts)
        if hasattr(nba, 'nuts'): bolts.extend(nba.nuts)
        if hasattr(nba, 'bolts_AF'): bolts.extend(nba.bolts_AF)
        if hasattr(nba, 'nuts_AF'): bolts.extend(nba.nuts_AF)
        
    # 4. Welds (Strict filtering)
    # Also skip stiffener welds for flushed/one-way variants
    weld_skipped_patterns = []
    if is_flushed:
        weld_skipped_patterns = ['bbWeldStiffHL_', 'bbWeldStiffHR_', 'bbWeldStiffLL_', 'bbWeldStiffLR_', 'bcWeldStiff']
    elif is_oneway:
        if is_bc_endplate:
            # BCEndplate: _2 is bottom
            weld_skipped_patterns = ['bcWeldStiffHL_2', 'bcWeldStiffHR_2', 'bcWeldStiffLL_2', 'bcWeldStiffLR_2']
        else:
            # BBEndplate (Splice): _2, _4 are bottom
            weld_skipped_patterns = ['bbWeldStiffHL_2', 'bbWeldStiffHL_4', 'bbWeldStiffHR_2', 'bbWeldStiffHR_4',
                                      'bbWeldStiffLL_2', 'bbWeldStiffLL_4', 'bbWeldStiffLR_2', 'bbWeldStiffLR_4',
                                      'bcWeldStiffHL_2', 'bcWeldStiffHR_2', 'bcWeldStiffLL_2', 'bcWeldStiffLR_2']

    for attr in sorted(dir(cad_obj)):
        if attr.startswith('_'): continue
        if (is_flushed or is_oneway) and any(attr.startswith(p) for p in weld_skipped_patterns): continue
        
        if attr.endswith('Model') or attr.endswith('_Model'):
            base_attr = attr.replace('Model', '').replace('_Model', '')
            if base_attr in handled_names: continue
            if getattr(cad_obj, attr) is None: continue
            val = getattr(cad_obj, base_attr, None)
            if val is not None and type(val).__name__ in ('FilletWeld', 'GrooveWeld', 'Weld', 'Weld_sec'):
                welds.append(val)
                
    return members, plates, bolts, welds, others

def extract_moment_coverplate_bolted(cad_obj):
    """
    Explicit extractor for Moment Bolted Cover Plate splices.
    Handles CC Splice Bolted and BB Splice Bolted.
    """
    members = []
    plates = []
    bolts = []
    welds = []
    others = []
    
    # 1. Structural Members
    member_map = [
        ('column', 'columnModel'), ('column', 'column_Model'),
        ('column1', 'column1Model'), ('column1', 'column1_Model'),
        ('column2', 'column2Model'), ('column2', 'column2_Model'),
        ('beamLeft', 'beamLModel'), ('beamRight', 'beamRModel'),
        ('beam1', 'beam1Model'), ('beam1', 'beam1_Model'),
        ('beam2', 'beam2Model'), ('beam2', 'beam2_Model')
    ]
    for attr, model_attr in member_map:
        if getattr(cad_obj, model_attr, None) is not None:
            val = getattr(cad_obj, attr, None)
            if val is not None:
                members.append(val)
                
    # 2. Cover & Packing Plates
    plate_attrs = [
        'plateAbvFlange', 'plateBelwFlange', 'WebPlateLeft', 'WebPlateRight', # BB
        'innerplateAbvFlangeFront', 'innerplateAbvFlangeBack', 
        'innerplateBelwFlangeFront', 'innerplateBelwFlangeBack',
        'flangePlate1', 'flangePlate2', 'webPlate1', 'webPlate2', # CC
        'innerFlangePlate1', 'innerFlangePlate2', 'innerFlangePlate3', 'innerFlangePlate4'
    ]
    for attr in plate_attrs:
        model_name = next((attr + m for m in ['Model', '_Model'] if hasattr(cad_obj, attr + m)), None)
        if model_name and getattr(cad_obj, model_name) is not None:
            val = getattr(cad_obj, attr, None)
            if val is not None:
                plates.append(assign_ifc_name(val, attr, cad_obj.__class__.__name__))

    # 2b. Generic Plate Scan (for missed attributes or variant-specific names)
    handled_names = set(plate_attrs) | set([m[0] for m in member_map]) | {'weldCutPlate'}
    for attr in sorted(dir(cad_obj)):
        if attr.startswith('_') or attr in handled_names: continue
        if attr.endswith('Model') or attr.endswith('_Model'):
            base_attr = attr.replace('Model', '').replace('_Model', '')
            if base_attr in handled_names: continue
            if getattr(cad_obj, attr) is None: continue 
            val = getattr(cad_obj, base_attr, None)
            if val is not None and type(val).__name__ in ('Plate', 'StiffenerPlate', 'Stiffener', 'Angle'):
                plates.append(assign_ifc_name(val, base_attr, cad_obj.__class__.__name__))
                
    # 2c. Welds (Strict filtering)
    for attr in sorted(dir(cad_obj)):
        if attr.startswith('_'): continue
        if attr.endswith('Model') or attr.endswith('_Model'):
            base_attr = attr.replace('Model', '').replace('_Model', '')
            if base_attr in handled_names: continue
            if getattr(cad_obj, attr) is None: continue
            val = getattr(cad_obj, base_attr, None)
            if val is not None and type(val).__name__ in ('FilletWeld', 'GrooveWeld', 'Weld'):
                welds.append(val)
                
    # 3. Bolt Arrays (3 distinct zones)
    bolt_attrs = ['nut_bolt_array_AF', 'nut_bolt_array_BF', 'nut_bolt_array_Web']
    for attr in bolt_attrs:
        val = getattr(cad_obj, attr, None)
        if val is not None:
            # Unpack bolts and nuts from the array object
            if hasattr(val, 'bolts'): bolts.extend(val.bolts)
            if hasattr(val, 'nuts'): bolts.extend(val.nuts)
            # Module-specific naming in some Moment connections
            if hasattr(val, 'bolts_AF'): bolts.extend(val.bolts_AF)
            if hasattr(val, 'nuts_AF'): bolts.extend(val.nuts_AF)
            if hasattr(val, 'bolts_BF'): bolts.extend(val.bolts_BF)
            if hasattr(val, 'nuts_BF'): bolts.extend(val.nuts_BF)
            if hasattr(val, 'bolts_W'): bolts.extend(val.bolts_W)
            if hasattr(val, 'nuts_W'): bolts.extend(val.nuts_W)
                
    return members, plates, bolts, welds, others

def extract_moment_coverplate_welded(cad_obj):
    """
    Explicit extractor for Moment Welded Cover Plate splices.
    Handles CC Splice Welded and BB Splice Welded.
    """
    members = []
    plates = []
    bolts = []
    welds = []
    others = []
    
    # 1. Structural Members
    member_attrs = ['column', 'column1', 'column2', 'beam', 'beamLeft', 'beamRight', 'beam1', 'beam2']
    for attr in member_attrs:
        model_name = next((attr + m for m in ['Model', '_Model'] if hasattr(cad_obj, attr + m)), None)
        if model_name and getattr(cad_obj, model_name) is not None:
            val = getattr(cad_obj, attr, None)
            if val is not None:
                members.append(val)
                
    # 2. Plates
    plate_attrs = [
        'flangePlate', 'innerFlangePlate', 'webPlate', # Base references
        'flangePlate1', 'flangePlate2', 'webPlate1', 'webPlate2', # Instances
        'innerFlangePlate1', 'innerFlangePlate2', 'innerFlangePlate3', 'innerFlangePlate4'
    ]
    for attr in plate_attrs:
        model_name = next((attr + m for m in ['Model', '_Model'] if hasattr(cad_obj, attr + m)), None)
        if model_name and getattr(cad_obj, model_name) is not None:
            val = getattr(cad_obj, attr, None)
            if val is not None:
                plates.append(assign_ifc_name(val, attr, cad_obj.__class__.__name__))
                
    # 2b. Generic Plate Scan (for missed attributes or variant-specific names)
    handled_names = set(plate_attrs) | set(member_attrs) | {'weldCutPlate'}
    for attr in sorted(dir(cad_obj)):
        if attr.startswith('_') or attr in handled_names: continue
        if attr.endswith('Model') or attr.endswith('_Model'):
            base_attr = attr.replace('Model', '').replace('_Model', '')
            if base_attr in handled_names: continue
            if getattr(cad_obj, attr) is None: continue
            val = getattr(cad_obj, base_attr, None)
            if val is not None and type(val).__name__ in ('Plate', 'StiffenerPlate', 'Stiffener', 'Angle'):
                plates.append(assign_ifc_name(val, base_attr, cad_obj.__class__.__name__))

    # 4. Welds (Strict filtering)
    if hasattr(cad_obj, 'welds') and isinstance(cad_obj.welds, list):
        welds.extend(cad_obj.welds)
    else:
        # Fallback to scanning for initialized weld models
        for attr in sorted(dir(cad_obj)):
            if attr.startswith('_') or attr in handled_names:
                continue
            if attr.endswith('Model') or attr.endswith('_Model'):
                model_val = getattr(cad_obj, attr)
                if model_val is None: continue
                base_attr = attr.replace('Model', '').replace('_Model', '')
                val = getattr(cad_obj, base_attr, None)
                if val is not None and type(val).__name__ in ('FilletWeld', 'GrooveWeld', 'Weld'):
                    welds.append(val)
            
    return members, plates, bolts, welds, others

def extract_truss_connection(cad_obj):
    """
    Explicit extractor for Truss / Tension / Compression connections.
    Filters out unplaced template objects by checking model generation flags.
    """
    members = []
    plates = []
    bolts = []
    welds = []
    others = []
    
    # 1. Structural Members
    for attr in ['member1', 'member2']:
        if getattr(cad_obj, attr + '_Model', None) is not None:
            val = getattr(cad_obj, attr, None)
            if val is not None:
                members.append(val)
                
    if getattr(cad_obj, 'columnModel', None) is not None:
        val = getattr(cad_obj, 'sec', None)
        if val is not None:
            members.append(val)
                
    # 2. Gusset / End Plates
    for attr in ['plate1', 'plate2']:
        if getattr(cad_obj, attr + '_Model', None) is not None:
            val = getattr(cad_obj, attr, None)
            if val is not None:
                plates.append(assign_ifc_name(val, attr, cad_obj.__class__.__name__))
                
    # 3. Fasteners
    bolt_arrays = [
        ('nut_bolt_arrayL', 'nutboltArrayLModels'),
        ('nut_bolt_arrayR', 'nutboltArrayRModels'),
        ('nut_bolt_arrayL_SA', 'nutboltArrayL_SAModels'),
        ('nut_bolt_arrayR_SA', 'nutboltArrayR_SAModels')
    ]
    for attr, model_attr in bolt_arrays:
        if getattr(cad_obj, model_attr, None) is not None:
            nba = getattr(cad_obj, attr, None)
            if nba is not None and getattr(nba, 'origin', None) is not None:
                if hasattr(nba, 'bolts'): bolts.extend(nba.bolts)
                if hasattr(nba, 'nuts'): bolts.extend(nba.nuts)
                if hasattr(nba, 'boltsabv'): bolts.extend(nba.boltsabv)
                if hasattr(nba, 'nutsabv'): bolts.extend(nba.nutsabv)
                
    # Fasteners / Plates from Intermittent Connections
    if getattr(cad_obj, 'intermittentConnection_Model', None) is not None:
        ic = getattr(cad_obj, 'intermittentConnection', None)
        if ic is not None:
            if hasattr(ic, 'plates'):
                for p_idx, p_val in enumerate(ic.plates):
                    plates.append(assign_ifc_name(p_val, f"intermittentPlate{p_idx+1}", cad_obj.__class__.__name__))
            if hasattr(ic, 'bolts'): bolts.extend(ic.bolts)
            if hasattr(ic, 'nuts'): bolts.extend(ic.nuts)
            if hasattr(ic, 'boltsabv'): bolts.extend(ic.boltsabv)
            if hasattr(ic, 'nutsabv'): bolts.extend(ic.nutsabv)
            if hasattr(ic, 'weldsabw'): welds.extend(ic.weldsabw)
            if hasattr(ic, 'weldsblw'): welds.extend(ic.weldsblw)
            if hasattr(ic, 'weldsabw1'): welds.extend(ic.weldsabw1)
            if hasattr(ic, 'weldsblw1'): welds.extend(ic.weldsblw1)
                
    # 4. Welds (Strict filtering)
    weld_attrs = [
        'weldHL11', 'weldHL12', 'weldHR11', 'weldHR12', 'weldVL11', 'weldVR11',
        'weldHL21', 'weldHL22', 'weldHR21', 'weldHR22', 'weldVL21', 'weldVR21'
    ]
    for attr in weld_attrs:
        if getattr(cad_obj, attr + '_Model', None) is not None:
            val = getattr(cad_obj, attr, None)
            if val is not None:
                welds.append(val)
            
    return members, plates, bolts, welds, others

# ─────────────────────────────────────────────────────────────────────────────
# JSON Serializer & Metadata Extractor
# ─────────────────────────────────────────────────────────────────────────────

def obj_to_dict(obj):
    """
    Serialize an OSDAG CAD primitive object into a JSON-compatible dictionary.
    Captures all numeric, string, boolean, and ndarray properties.
    """
    d = {'_class_name': type(obj).__name__}
    for k in dir(obj):
        if not k.startswith('_') and k not in ('create_model', 'place', 'compute_params', 'getPoint'):
            try:
                val = getattr(obj, k)
                if isinstance(val, (int, float, str, bool)):
                    d[k] = val
                elif type(val).__name__ == 'ndarray':
                    d[k] = val.tolist()
            except Exception:
                pass
    return d

def extract_metadata(module_obj, design_dict=None):
    """
    Extracts non-geometric engineering properties (loads, material, status)
    for Pset_OsdagDesignData.
    """
    meta = {}
    if design_dict:
        material = design_dict.get('Member.Material') or design_dict.get('Material')
        if material: meta['Material'] = str(material)

        profile = design_dict.get('Member.Profile') or design_dict.get('Member.Designation')
        if profile: meta['Profile'] = str(profile)
        
        # Globally extract all possible structural profile strings
        supp = design_dict.get('Supporting_Section.Designation') or design_dict.get('Column.Designation')
        if supp: meta['Supporting_Profile'] = str(supp).strip()
        
        suptd = design_dict.get('Supported_Section.Designation') or design_dict.get('Beam.Designation')
        if suptd: meta['Supported_Profile'] = str(suptd).strip()
        
        base_desig = design_dict.get('Section.Designation')
        if base_desig: meta['Section_Profile'] = str(base_desig).strip()

        for k, v in design_dict.items():
            k_str = str(k).replace('\xa0', ' ')
            if 'Axial' in k_str:
                try: meta['AxialForce_kN'] = float(v)
                except: pass
            elif 'Shear' in k_str:
                try: meta['ShearForce_kN'] = float(v)
                except: pass
            elif 'Moment' in k_str:
                try: meta['Moment_kNm'] = float(v)
                except: pass

        if 'Module' in design_dict:
            meta['ConnectionType'] = str(design_dict['Module'])

    meta['DesignStatus'] = str(getattr(module_obj, 'design_status', 'Unknown'))
    return meta

# ─────────────────────────────────────────────────────────────────────────────
# Unified Dispatcher
# ─────────────────────────────────────────────────────────────────────────────

DISPATCH_MAP = {
    # Simple Plated
    'BoltedLapJointCAD': extract_simple_plated,
    'WeldedLapJointCAD': extract_simple_plated,
    'BoltedButtJointCAD': extract_simple_plated,
    'WeldedButtJointCAD': extract_simple_plated,
    
    # Shear Connections
    'FinPlateCAD': extract_shear_connections,
    'CleatAngleCAD': extract_shear_connections,
    'HeaderPlateCAD': extract_shear_connections, 
    'SeatedAngleCAD': extract_shear_connections,
    'ColFlangeBeamWeb': extract_shear_connections,
    'ColWebBeamWeb': extract_shear_connections,
    'BeamWebBeamWeb': extract_shear_connections,
    
    # Base Plates
    'BasePlateCad': extract_base_plate,
    'HollowBasePlateCad': extract_base_plate,
    
    # Moment End Plate Variations
    'CADGroove': extract_moment_endplate,       
    'CADFillet': extract_moment_endplate,       
    'CADcolwebGroove': extract_moment_endplate, 
    'CADColWebFillet': extract_moment_endplate, 
    'CCEndPlateCAD': extract_moment_endplate,   
    
    # Moment Cover Plate Variations
    'CCSpliceCoverPlateBoltedCAD': extract_moment_coverplate_bolted,
    'BBCoverPlateBoltedCAD': extract_moment_coverplate_bolted,
    'CCSpliceCoverPlateWeldedCAD': extract_moment_coverplate_welded,
    'BBSpliceCoverPlateWeldedCAD': extract_moment_coverplate_welded,
    
    # Truss / Tension / Compression
    'TensionAngleBoltCAD': extract_truss_connection,
    'TensionChannelBoltCAD': extract_truss_connection,
    'TensionAngleWeldCAD': extract_truss_connection,
    'TensionChannelWeldCAD': extract_truss_connection,
    'StrutAngleBoltCAD': extract_truss_connection,
    'StrutChannelBoltCAD': extract_truss_connection,
    'StrutAngleWeldCAD': extract_truss_connection,
    'StrutChannelWeldCAD': extract_truss_connection,
    'CompressionMemberCAD': extract_truss_connection,
}

def extract_cad_items(cad_obj):
    """
    Unified entry point: given any OSDAG CAD object, automatically detect its
    type and dispatch to the highly explicit extractors that safely isolate
    members, plates, bolts, and welds according to its exact internal structure.
    """
    cad_class = type(cad_obj).__name__
    
    if cad_class in DISPATCH_MAP:
        return DISPATCH_MAP[cad_class](cad_obj)
        
    print(f"Warning: Unmapped CAD Class: '{cad_class}'. Falling back to safe empty geometry sets.")
    return [], [], [], [], []
