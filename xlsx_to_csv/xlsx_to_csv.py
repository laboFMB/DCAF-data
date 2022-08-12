import pandas as pd
import argparse


def xlsx_to_csv(excel_file_path: str, csv_file_path: str) -> None:
    excel_dataframe = pd.read_excel(excel_file_path)
    excel_dataframe.to_csv(csv_file_path, index=None, header=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert excel files to csv")
    parser.add_argument('excel_file', type=str,
                        help="path to input excel files")
    parser.add_argument('csv_file', type=str, help="path to output csv file")
    args = parser.parse_args()
    xlsx_to_csv(args.excel_file, args.csv_file)
