"""
Command-line interface for running Osdag modules programmatically.
"""
from pathlib import Path
import yaml
from .Command_line import available_module


class ResultDict:
    """Dictionary-like object that supports both dict and attribute access."""
    def __init__(self, data):
        self._data = data if isinstance(data, dict) else {}
    
    def __getitem__(self, key):
        return self._data[key]
    
    def __getattr__(self, key):
        try:
            return self._data[key]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")
    
    def get(self, key, default=None):
        return self._data.get(key, default)
    
    def __contains__(self, key):
        return key in self._data
    
    def __repr__(self):
        return f"ResultDict({self._data})"


def run_module(input_file):
    """
    Run an Osdag module with the given input file.
    
    Args:
        input_file: Path to the .osi input file (Path object or string)
    
    Returns:
        ResultDict: Dictionary-like object containing module results
    """
    # Convert to Path if needed
    if isinstance(input_file, str):
        input_file = Path(input_file)
    elif not isinstance(input_file, Path):
        input_file = Path(input_file)
    
    # Read input file
    with open(input_file, 'r') as f:
        design_data = yaml.safe_load(f)
    
    # Get module name from input data
    module_name = design_data.get('Module')
    if not module_name:
        raise ValueError(f"No 'Module' field found in input file: {input_file}")
    
    if module_name not in available_module:
        raise ValueError(f"Module '{module_name}' not found in available modules")
    
    # Get module class and instantiate
    module_class = available_module[module_name]
    module_obj = module_class()
    
    # Set logger and input values
    # Some modules (e.g., Tension_welded) have set_osdaglogger() with no arguments
    import inspect
    sig = inspect.signature(module_obj.set_osdaglogger)
    if len(sig.parameters) == 0:
        module_obj.set_osdaglogger()
    else:
        module_obj.set_osdaglogger(None)
    module_obj.set_input_values(design_data)
    
    # Run the design (if method exists)
    if hasattr(module_obj, 'trial_design'):
        module_obj.trial_design()
    elif hasattr(module_obj, 'design'):
        module_obj.design()
    
    # Get results
    results = {}
    if hasattr(module_obj, 'results_to_test'):
        results_dict = module_obj.results_to_test(module_obj)
        if isinstance(results_dict, dict):
            results = results_dict
        elif isinstance(results_dict, list) and len(results_dict) > 0:
            # Some modules return a list, extract the first result row
            if isinstance(results_dict[0], (list, tuple)) and len(results_dict[0]) > 2:
                # Extract designation, bolt_rows, bolt_columns from result list
                results = {
                    'designation': results_dict[0][2] if len(results_dict[0]) > 2 else None,
                    'bolt_rows': results_dict[0][5] if len(results_dict[0]) > 5 else None,
                    'bolt_columns': results_dict[0][6] if len(results_dict[0]) > 6 else None,
                }
    
    # Also try to get attributes directly from the module object
    if 'designation' not in results:
        if hasattr(module_obj, 'designation'):
            results['designation'] = getattr(module_obj, 'designation', None)
        elif hasattr(module_obj, 'cleat') and hasattr(module_obj.cleat, 'designation'):
            results['designation'] = module_obj.cleat.designation
        elif hasattr(module_obj, 'plate') and hasattr(module_obj.plate, 'designation'):
            results['designation'] = module_obj.plate.designation
    
    if 'bolt_rows' not in results:
        if hasattr(module_obj, 'bolt_rows'):
            results['bolt_rows'] = getattr(module_obj, 'bolt_rows', None)
        elif hasattr(module_obj, 'sptd_leg') and hasattr(module_obj.sptd_leg, 'bolts_one_line'):
            results['bolt_rows'] = module_obj.sptd_leg.bolts_one_line
        elif hasattr(module_obj, 'plate') and hasattr(module_obj.plate, 'bolts_one_line'):
            results['bolt_rows'] = module_obj.plate.bolts_one_line
        elif hasattr(module_obj, 'bolt') and hasattr(module_obj.bolt, 'bolt_row'):
            results['bolt_rows'] = module_obj.bolt.bolt_row
    
    if 'bolt_columns' not in results:
        if hasattr(module_obj, 'bolt_columns'):
            results['bolt_columns'] = getattr(module_obj, 'bolt_columns', None)
        elif hasattr(module_obj, 'sptd_leg') and hasattr(module_obj.sptd_leg, 'bolt_line'):
            results['bolt_columns'] = module_obj.sptd_leg.bolt_line
        elif hasattr(module_obj, 'plate') and hasattr(module_obj.plate, 'bolt_line'):
            results['bolt_columns'] = module_obj.plate.bolt_line
        elif hasattr(module_obj, 'bolt') and hasattr(module_obj.bolt, 'bolt_col'):
            results['bolt_columns'] = module_obj.bolt.bolt_col
    
    return ResultDict(results)
