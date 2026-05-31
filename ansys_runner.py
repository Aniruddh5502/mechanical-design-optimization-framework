"""
Ansys Workbench Runner - Inline function to update parameters
"""

import json

def run_solver(input_params: dict, wb):
    params_mapping = {
        "beam_length": "P5",
        "beam_height": "P1",
        "beam_width_1": "P4",
        "beam_width_2": "P3",
        "fillet_size": "P6"
    }
    
    # Build script to update parameters using f-string
    script = f"""
import json

try:
    # Update input parameters
    
    beam_length_param = Parameters.GetParameter(Name="{params_mapping['beam_length']}")
    beam_length_param.Expression = "{input_params['beam_length']} [mm]"
    
    beam_height_param = Parameters.GetParameter(Name="{params_mapping['beam_height']}")
    beam_height_param.Expression = "{input_params['beam_height']} [mm]"
    
    beam_width_1_param = Parameters.GetParameter(Name="{params_mapping['beam_width_1']}")
    beam_width_1_param.Expression = "{input_params['beam_width']} [mm]"
    
    beam_width_2_param = Parameters.GetParameter(Name="{params_mapping['beam_width_2']}")
    beam_width_2_param.Expression = "{input_params['beam_width']} [mm]"
    
    fillet_size_param = Parameters.GetParameter(Name="{params_mapping['fillet_size']}")
    fillet_size_param.Expression = "{input_params['fillet_size']} [mm]"
    
    # Update the design point
    backgroundSession = UpdateAllDesignPoints(DesignPoints=[Parameters.GetDesignPoint(Name="0")])
    #Save()
    
    Update()
    # Get output parameters
    output_params = {{}}
    
    # P7-P12 are typically output parameters
    output_param_names = ['P7', 'P8', 'P9', 'P10', 'P11', 'P12']
    for param_name in output_param_names:
        try:
            p = Parameters.GetParameter(Name=param_name)
            if p:
                output_params[param_name] = str(p.Value)
        except:
            output_params[param_name] = None
    
    result = {{
        'success': True,
        'output_parameters': output_params
    }}
    
except Exception as e:
    result = {{
        'success': False,
        'error': str(e)
    }}

wb_script_result = json.dumps(result)
"""
    
    # Run the script and return result
    return wb.run_script_string(script)


