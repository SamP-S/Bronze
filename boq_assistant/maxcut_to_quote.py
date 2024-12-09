import os
import pandas as pd
import numpy as np
import argparse
import csv

# loads template xlsx file and returns sheets as dictionary of pd.DataFrames or empty dictionary if failed
### TODO:
# copy template xlsx to output path then write new qto sheets to it
# means existing formatting will be preserved instead of getting trunced by dataframe
def get_template_sheets():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, "template.xlsx")
    try:
        xl = pd.ExcelFile(template_path)
        template_sheets = pd.read_excel(xl, sheet_name=None)
        print(f"INFO: Found template sheets.\n{template_sheets.keys()}")
        # print(type(template_sheets))
        # print(type(template_sheets["Front Cover"]))
        xl.close()
        return template_sheets
    except Exception as err:
        print(f"WARNING: Couldn't open template, skipping...\n{err}")
        return {}

def maxcut_to_quote(input_path, output_path):
    output_dir = os.path.dirname(os.path.abspath(output_path))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"INFO: Created output directory.\n{output_dir}")

    if not os.path.exists(input_path):
        return f"ERROR: Can't find input file.\n{input_path}"
        
    if not input_path.endswith(".csv"):
        return f"ERROR: input file is not CSV file.\n{input_path}"
    
    # attempt to load csv
    df = None
    try:
        df = pd.read_csv(args.filepath)
    except Exception as err:
        return f"ERROR: Couldn't open file.\n{input_path}\n {err}\nPlease close the file if you have it opened in excel."
    
    
    print(df.head(10))
    template_sheets = get_template_sheets()
    
    ### CONTINUE:


### IMPORTANT IMPLEMENTATION NOTES:
# "./template.xlsx" hold "Front Cover", "Quote" and "Allowances" sheets to copy into generated quote.
# It is assumed all relevant maxcut input items are contained in a single csv file.
# Input items will be seperated by material into respective QTO sheets.
# Groups should be used to determine which room a material belongs to, if no groups found, all materials will be assumed to be in a single unspecified room.
# All input items of type "labour" and "hardware" will be ignored.
# TODO: Accept edging
# TODO: Support .mc3 files

parser = argparse.ArgumentParser(
    prog="scs_quote_to_maxcut",
    description="convert quote sheet from .xlsx to maxcut .csv"
)

# Required arguments
parser.add_argument("filepath")
# Optional arguments
parser.add_argument("-o", "--output", help="output directory")

args = parser.parse_args()

# set default output path
base_path, _ = args.filepath.rsplit(".", 1)
output_path = base_path + f"_quote.xlsx"
# use given output path if provided
if not args.output is None:
    output_path = os.path.abspath(args.output)

# check for output overwrite
if os.path.exists(output_path):
    print(f"WARNING: File already exists. Should I overwrite it?\n{output_path}")
    user_input = input("y/n")
    if user_input == "y":
        print(f"INFO: Will overwrite file.\n{output_path}")
    else:
        print("INFO: Exiting.")
        exit(0)

# check for input file
if not os.path.exists(args.filepath):
    print(f"ERROR: Can't find input file.\n{args.filepath}")
    exit(1)
    
# check input file type
if not args.filepath.endswith(".csv"):
    print(f"ERROR: input file is not CSV file.\n{args.filepath}")
    exit(1)

# convert maxcut csv to quote xlsx
err = maxcut_to_quote(args.filepath, output_path)
if err is None:
    print(f"INFO: Conversion successful. Output written to:\n{output_path}")
else:
    print(f"ERROR: Conversion failed.\n{err}")
    exit(1)
