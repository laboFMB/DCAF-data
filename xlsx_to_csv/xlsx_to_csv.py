import pandas as pd
import argparse
import glob
import os


def xlsx_to_csv(excel_file_path: str, csv_file_path: str) -> None:
    excel_dataframe = pd.read_excel(excel_file_path)
    excel_dataframe.to_csv(csv_file_path, index=None, header=True)

def change_ext_to_csv(xlsx_name):
    return xlsx_name.replace(".xlsx", ".csv")

def find_all_xlsx(directory):
    return glob.glob(os.path.join(directory, '**/*.xlsx'), recursive = True)

def convert_all_xlsx(xlsx_list):
    csv_names = map(change_ext_to_csv, xlsx_list)
    for xlsx_name, csv_name in zip(xlsx_list, csv_names):
        xlsx_to_csv(xlsx_name, csv_name)

def main(directory):
    xlsx_list = find_all_xlsx(directory)
    convert_all_xlsx(xlsx_list)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert excel files to csv")
    parser.add_argument('directory', type=str,
                        help="will convert all files in directory recursively")
    args = parser.parse_args()
    main(args.directory)
