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

parser.add_argument("filepath")
parser.add_argument("sheet_name")
parser.add_argument("material")
# parser.add_argument("max_row")

# TODO: implement optional output directory

args = parser.parse_args()

if not os.path.exists(args.filepath):
    print("ERROR: Can't find input file.")
    exit(1)
    
if not args.filepath.endswith(".xlsx"):
    print("ERROR: input file is not Excel file.")
    exit(1)

# if not args.max_row.isdigit():
#     print("ERROR: max row is not whole number.")
# max_row = int(args.max_row)

xl = None
try:
    xl = pd.ExcelFile(args.filepath)
except Exception as err:
    print(f"ERROR: Couldn't open file:\n {err}")
    print("Please close the file if you have it opened in excel.")
    exit(1)

# pass None to load all sheets
sheets = pd.read_excel(xl, sheet_name=None)
if not args.sheet_name in sheets:
    print(f"ERROR: No sheet named {args.sheet_name} in excel file")
    exit(1)
    
# parse dataframe
df = sheets[args.sheet_name]

# TODO: support lower case
max_row_options = df.index[df["Name"] == "Description"].tolist()
if (len(max_row_options) == 0):
    print(f"ERROR: Can't autodetect max row num")
    exit(1)
max_row = max_row_options[0]
if (max_row == 0):
    print(f"ERROR: Max row autodetect failed. max_row = {max_row}")
    exit(1)
max_row -= 1

df = df.head(int(max_row))
df = df[["Name", "Length", "Width", "Quantity"]]
df["Material"] = [args.material for i in range(max_row)]

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
        print(f"WARNING: Failed to comma check names. idx = {i}; name = {row["Name"]};")
    
# print(df["Name"])

# make output path
base_path, _ = args.filepath.rsplit(".", 1)
out_path = base_path + f"_{args.sheet_name}.csv"


# TODO: look more into csv.QUOTE_NONE and stuff to try allow commas
# NOTE: might not be important at all though
try:
    df.to_csv(out_path, index=False)
    print(f"Successfully output to: {out_path}")
except Exception as e:
    print(f"ERROR: Failed to write to: {out_path}")
    exit(1)




