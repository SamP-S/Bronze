import os
import pandas as pd
import numpy as np
import argparse
import csv
import zipfile

def _pathlist_to_zip(pathlist, output_path):
    if os.path.exists(output_path):
        print(f"WARNING: Output file already exists. Overwriting...\n{output_path}")
    with open(output_path, "wb") as f:
        with zipfile.ZipFile(f, "w") as z:
            for path in pathlist:
                if (path is None) or (not os.path.exists(path)):
                    print(f"WARNING: Path not found. Skipping...\n{path}")
                    continue
                # set arcname to filename only, dont copy full dir path
                z.write(path, os.path.basename(path))
    return output_path

def _qto_get_meta(df):
    if ("Name" not in df.columns):
        print("ERROR: Name not found in columns")
        return None, None
        
    max_row_options = df.index[df["Name"] == "Description"].tolist()
    if (len(max_row_options) == 0):
        print(f"ERROR: Can't autodetect max row num")
        return None, None
    max_row = max_row_options[0]
    if (max_row == 0):
        print(f"ERROR: Max row autodetect failed. max_row = {max_row}")
        return None, None
    max_row -= 1
    material = df.at[max_row + 2, "Name"]
    print(f"INFO: Found material: {material}")
    return max_row, material


def _qto_order_length_width(df):
    if ("Length" not in df.columns) or ("Width" not in df.columns):
        print("ERROR: Length or Width not found in columns")
        return None
    
    for i, row in df.iterrows():
        length, width = row[["Length", "Width"]]
        if (width > length):
            df.at[i,"Length"] = width
            df.at[i, "Width"] = length
    return df
    
# parse dataframe to maxcut csv
# returns output path if successful, else returns None
def qto_to_maxcut_csv(df, output_path):
    print()
    # search for max row by finding "Description" keyword
    ### TODO: support lower case
    max_row, material = _qto_get_meta(df)
    if (max_row is None) or (material is None):
        print("ERROR: Failed to autodetect max row & material meta data.")
        return None

    df = df.head(int(max_row))
    df = df[["Name", "Length", "Width", "Quantity"]]
    df["Material"] = [material for i in range(max_row)]

    # TODO: consider what empty/invalid data should be deleted
    df = df[df["Length"].notna()]
    df = df[df["Width"].notna()]

    df = _qto_order_length_width(df)
    if (df is None):
        print("ERROR: Failed to order length > width.")
        return None
            
    for i, row in df.iterrows():
        try:
            df.at[i, "Name"] = row["Name"].replace(",", " +")
        except Exception as e:
            print(f"WARNING: Failed to comma check names. idx = {i}; name = {row["Name"]};")
            return None


    # TODO: look more into csv.QUOTE_NONE and stuff to try allow commas
    # NOTE: might not be important at all though
    try:
        df.to_csv(output_path, index=False)
        print(f"INFO: Successfully output to: {output_path}")
        return output_path
    except Exception as e:
        print(f"ERROR: Failed to write to: {output_path}")
        return None

# TODO: make it delete csv files generated after zipping
# TODO: convert ouput_path arg to output_path and tmp_dir
# returns path of successful zip output path or None
def quote_to_maxcut(input_path, output_path=None, sheet_names=None):
    # input file verification
    if not os.path.exists(input_path):
        print(f"ERROR: Can't find input file.\n{input_path}")
        return None
    if not input_path.endswith(".xlsx"):
        print(f"ERROR: input file is not Excel file.\n{input_path}")
        return None
    
    xl = None
    try:
        xl = pd.ExcelFile(input_path)
    except Exception as err:
        print(f"ERROR: Couldn't open file.\n {err}")
        print("Please close the file if you have it opened in excel.")
        return None
    
    # output directory verification
    output_dir = os.path.dirname(input_path)
    if not output_path is None:
        print(f"INFO: No output directory set. Using default.\n{output_dir}")
        output_dir = output_path
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"INFO: Output path parent directory not found. Creating output directory.\n{output_dir}")


    
    # sheet selection
    # TODO: improve this garbage
    sheets = pd.read_excel(xl, sheet_name=None)
    print(f"INFO: found sheets: {sheets.keys()}")
    print(f"INFO: requested sheets: {sheet_names}")
    if (sheet_names is None) or len(sheet_names) == 0:
        print("INFO: No sheets requested. Processing all sheets instead.")
        sheet_names = list(sheets.keys())
        
    for sheet_name in sheet_names:
        if sheet_name not in sheets.keys():
            print(f"WARNING: Sheet '{sheet_name}' not found in file. Skipping...")
            sheet_names.remove(sheet_name)
        
    ignore_sheets = [
        "Front Cover", "Allowances", "Quote",
        "Tiling", "Stone", "Cover Sheet",
    ]
    ignore_sheets = [x.lower() for x in ignore_sheets]
    for key in sheet_names:
        print(f"CHECK: {key.lower()} in {ignore_sheets}")
        if key.lower() in ignore_sheets:
            print(f"INFO: Ignoring sheet '{key}'. Skipping...")
            sheet_names.remove(key)
    print(f"INFO: Sheets to process: {sheet_names}")
            
    # make output file name
    filename_ext = os.path.splitext(os.path.basename(input_path))
        
    # main conversion loop
    succ_paths = []
    for key in sheet_names:
        df = sheets[key]
    
        base_filename = filename_ext[0]
        save_path = os.path.join(output_dir, f"{base_filename}_{key}.csv")
        print(base_filename)
        
        print(f"INFO: Attempting sheet {key}.\nOutput to: {save_path}")
        path = qto_to_maxcut_csv(df, save_path)
        if not(path is None):
            succ_paths.append(path)
        else:
            print(f"WARNING: Failed to convert sheet {key}.")
    
    zip_path = os.path.join(output_dir, f"{base_filename}_maxcut.zip")
    _pathlist_to_zip(succ_paths, zip_path)
    return zip_path   


### IMPORTANT IMPLEMENTATION NOTES:
# The keyword searched for in each respective cut list sheet is "Description", if not found, no output will be generated and a warning returned.
# The material name is grabbed from the cell below description, if not found, a dummy name will be put in that MaxCut will ask you to assign
# Sheets named "Front Cover", "Allowances" and "Quote" will be ignored. All other sheets will be assumed to be a cut list.
# Specific sheet names can be requested instead of all sheets, using the -s flag. If no sheets are requested, all sheets will be processed.
# The output directory can be specified using the -o flag. If not specified, the output will be in the same directory as the input file.
# The output file will be named the same as the input file, with the sheet name appended to the end with an "_".
# It is recommended sheet names are simple i.e. STxx.
    
def main():
    parser = argparse.ArgumentParser(
        prog="scs_quote_to_maxcut",
        description="convert quote sheet from .xlsx to maxcut .csv"
    )

    parser.add_argument("filepath")
    # either zero or more sheest
    parser.add_argument("-s", "--sheets", help="sheet name", nargs="*", default=[])
    parser.add_argument("-o", "--output", help="output directory")
    args = parser.parse_args()
    
    succ_paths = quote_to_maxcut(args.filepath, args.output, args.sheets)
    print(f"INFO: Successfully converted {len(succ_paths)} sheets.\n{succ_paths}")

if __name__ == "__main__":
    main()