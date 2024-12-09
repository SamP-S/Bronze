import os
import pandas as pd
import numpy as np
import argparse
import csv

# "C:\Users\Sam\OneDrive - South Coast Stone\Documents\Sam 43 Orchard Court\43 Orchard Court Complete Quote.xlsx"

parser = argparse.ArgumentParser(
    prog="scs_quote_to_maxcut",
    description="convert quote sheet from .xlsx to maxcut .csv"
)

### IMPORTANT IMPLEMENTATION NOTES:
# The keyword searched for in each respective cut list sheet is "Description", if not found, no output will be generated and a warning returned.
# The material name is grabbed from the cell below description, if not found, a dummy name will be put in that MaxCut will ask you to assign
# Sheets named "Front Cover", "Allowances" and "Quote" will be ignored. All other sheets will be assumed to be a cut list.
# Specific sheet names can be requested instead of all sheets, using the -s flag. If no sheets are requested, all sheets will be processed.
# The output directory can be specified using the -o flag. If not specified, the output will be in the same directory as the input file.
# The output file will be named the same as the input file, with the sheet name appended to the end with an "_".
# It is recommended sheet names are simple i.e. STxx.

parser.add_argument("filepath")
# either zero or more sheest
parser.add_argument("-s", "--sheets", help="sheet name", nargs="*", default=[])
parser.add_argument("-o", "--output", help="output directory")


# TODO: implement optional output directory

args = parser.parse_args()

output_dir = os.path.dirname(os.path.abspath(args.filepath))
if not args.output is None:
    output_dir = os.path.abspath(args.output)

if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    print(f"INFO: Created output directory.\n{output_dir}")

if not os.path.exists(args.filepath):
    print(f"ERROR: Can't find input file.\n{args.filepath}")
    exit(1)
    
if not args.filepath.endswith(".xlsx"):
    print(f"ERROR: input file is not Excel file.\n{args.filepath}")
    exit(1)

xl = None
try:
    xl = pd.ExcelFile(args.filepath)
except Exception as err:
    print(f"ERROR: Couldn't open file.\n {err}")
    print("Please close the file if you have it opened in excel.")
    exit(1)


# pass None to load all sheets
sheets = pd.read_excel(xl, sheet_name=None)
print(f"INFO: sheets: {sheets.keys()}")
sheets.pop("Quote", None)
sheets.pop("Allowances", None)
sheets.pop("Front Cover", None)

# parse dataframe to maxcut csv
def qto_to_maxcut_csv(df, output_path):
    # search for max row by finding "Description" keyword
    ### TODO: support lower case
    max_row_options = df.index[df["Name"] == "Description"].tolist()
    if (len(max_row_options) == 0):
        return f"ERROR: Can't autodetect max row num"
    max_row = max_row_options[0]
    if (max_row == 0):
        return f"ERROR: Max row autodetect failed. max_row = {max_row}"
    max_row -= 1
    material = df.at[max_row + 2, "Name"]
    print(material)

    df = df.head(int(max_row))
    df = df[["Name", "Length", "Width", "Quantity"]]
    df["Material"] = [material for i in range(max_row)]

    # TODO: consider what empty/invalid data should be deleted
    df = df[df["Length"].notna()]
    df = df[df["Width"].notna()]

    for i, row in df.iterrows():
        length, width = row[["Length", "Width"]]
        if (width > length):
            df.at[i,"Length"] = width
            df.at[i, "Width"] = length
            
    for i, row in df.iterrows():
        length, width = row[["Length", "Width"]]
        if (width > length):
            df.at[i,"Length"] = width
            df.at[i, "Width"] = length
            
    for i, row in df.iterrows():
        try:
            df.at[i, "Name"] = row["Name"].replace(",", " +")
        except Exception as e:
            return f"WARNING: Failed to comma check names. idx = {i}; name = {row["Name"]};"


    # TODO: look more into csv.QUOTE_NONE and stuff to try allow commas
    # NOTE: might not be important at all though
    try:
        df.to_csv(output_path, index=False)
        print(f"Successfully output to: {out_path}")
        return None
    except Exception as e:
        return f"ERROR: Failed to write to: {out_path}"


for key in sheets:
    df = sheets[key]
    
    # make output path
    base_path, _ = args.filepath.rsplit(".", 1)
    out_path = base_path + f"_{key}.csv"
    
    print(f"INFO: Attempting sheet {key}.\nOutput to: {out_path}")
    err = qto_to_maxcut_csv(df, out_path)
    if not err is None:
        print(err)

