import logging
import builtins
from pathlib import Path
from clean_logs import ROOT

# Store original print
original_print = builtins.print

# Override print
def print(*args, **kwargs):
    message = " ".join(str(arg) for arg in args)
    logging.info(message)
    original_print(*args, **kwargs)




try:
    import termcolor
    from termcolor import colored
    import os
    import re
    import numpy as np
    import pandas as pd
    pd.set_option('display.width', 2000)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    import itertools
    print("[ ",colored("x","green")," ]","    Library Importing Succesfull.")
except:
    print("[ ",colored("x","red")," ]","    Library Importing Failed.")


dataset_path    =   ROOT / "dataset/dataset.csv"
parameter_path  =   ROOT / "ansys_files/parameters.csv"



# Store original print
original_print = builtins.print

# Override print
def print(*args, **kwargs):
    message = " ".join(str(arg) for arg in args)
    logging.info(message)
    original_print(*args, **kwargs)




# ---------------------------------------------------------------------
#    EXTRACT THE PARAMETERS
# ---------------------------------------------------------------------

with open(parameter_path, "r") as f:
    lines = f.readlines()
    
param_line = None
for i, line in enumerate(lines):
    if "The parameters defined in the project are" in line:
        # search next lines for first line containing P1
        for next_line in lines[i+1:]:
            if "P1" in next_line:
                param_line = next_line
                break
        break


pattern =   r"(P\d+)\s*-\s*([^\[]+)"
matches =   re.findall(pattern, param_line)
if param_line is None:
    raise ValueError("[ x ]    Parameter definition line is not found.")

param_mapping = {code: name.strip() for code, name in matches}

# ------------------ LOAD NUMERIC TABLES ------------------------------
df = pd.read_csv(parameter_path, comment="#")
df.columns = df.columns.str.strip()

# Rename columns 
df = df.rename(columns = param_mapping)

# drop 'Name' columns
if "Name" in df.columns:
    df = df.drop(columns=['Name'])
    
print("[ ",colored("x","green")," ]","    parameter.csv parsed and loaded into dataframe.")
# Here df is the parameter table generated from the parameters.csv file exported 
# from the ansys workbench
# Now we merge the beam_width_1 and beam_width_2 in one column named 
# beam_width
df['beam_width'] = df[['beam_width_1','beam_width_2']].mean(axis=1)
# drop original beam width 1 and 2 columns
df = df.drop(columns=['beam_width_1','beam_width_2'])
print("[ ",colored("x","green")," ]","    beam_width_1 and beam_width_2 merged and made beam_width")
# Reorder column: 
cols = df.columns.tolist()
cols.remove('beam_width')  # remove from current position
insert_idx = cols.index('fillet_size') + 1
cols.insert(insert_idx, 'beam_width')
df = df[cols]
print("[ ",colored("x","green")," ]","    Columns re-ordered and saved to dataframe.")


n_levels = 6
bounds = {
    "fillet_size": (0.1000, 0.6000),
    "beam_width":  (0.4000, 0.8000),
    "beam_height": (5.0000, 20.000),
    "beam_length": (10.000, 17.000)
}

print("[ ",colored("x","green")," ]","    Iteration division is set to 5 between bounds")

input_cols = list(bounds.keys())
df.columns = df.columns.str.strip()

# ---------------------------------------------------------------------
# Generate input parameter grid
# ---------------------------------------------------------------------
param_values = {p: np.linspace(bounds[p][0], bounds[p][1], n_levels) for p in bounds}
all_points = list(itertools.product(*param_values.values()))
df_grid = pd.DataFrame(all_points, columns=input_cols)   

# ---------------------------------------------------------------------
# Create new DataFrame with same columns
# ---------------------------------------------------------------------
df_new = pd.DataFrame(columns=df.columns)

# Output columns are everything not in input_cols
output_cols = [c for c in df.columns if c not in input_cols]

# -----------------------------
# Populate using nested loop
# -----------------------------
rows = []

for i in range(len(df_grid)):
    row_dict = {col: df_grid.at[i, col] for col in input_cols}
    for col in output_cols:
        row_dict[col] = ""
    rows.append(row_dict)


df_new = pd.DataFrame(rows, columns=df.columns)   
df = df_new

df.to_csv(dataset_path, index=False)
print("[ ",colored("x","green")," ]","    The generated dataset is saved to : ",dataset_path)
# Info prints
print("[ ",colored("x","green")," ]","    Header of generated Dataset :\n")
print(df)