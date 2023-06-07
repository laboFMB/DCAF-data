import argparse
import glob
import os
import pandas as pd
import numpy as np
import traceback


def glob_pattern(directory, pattern):
    return glob.glob(os.path.join(directory, pattern), recursive=True)


def find_all_saintscore_xlsx(directory):
    return sorted(glob_pattern(directory, '**/*SaintScore*.xlsx'))


def find_all_intensity_xlsx(directory):
    return sorted(glob_pattern(directory, '**/*Intensity*.xlsx'))


def find_all_volcanoplot_xlsx(directory):
    return sorted(glob_pattern(directory, '**/*volcanoplot.xlsx'))


def safe_log2(array):
    np.seterr(divide='ignore')
    result = np.where(array != 0.0, np.log2(array), 0)
    np.seterr(divide='warn')
    return result


def get_file_pairs(saint_files, intensity_files):
    file_pairs = {}
    for saint_file in saint_files:
        dirname = os.path.dirname(saint_file)
        file_pairs[dirname] = [saint_file]
    for intensity_file in intensity_files:
        dirname = os.path.dirname(intensity_file)
        file_pairs[dirname].append(intensity_file)
    return file_pairs


def generate_saint_df(saint_file):
    saint_df = pd.read_excel(saint_file)

    bait = saint_df['Bait'].replace('^X', '', regex=True)
    prey_gene = saint_df['PreyGene'].str.upper()
    saint_score = saint_df['SaintScore']
    log_2_fc = safe_log2(saint_df['FoldChange'])

    return pd.DataFrame({"Bait": bait, "Prey Gene": prey_gene, "Saint Score": saint_score, "log2FC": log_2_fc})


def generate_volcano_df(volcano_file):
    volcano_df = pd.read_excel(volcano_file, sheet_name="Feature Meta Data")
    volcano_df.columns.values[1] = "log2FC"
    volcano_df.columns.values[2] = "pvalue"

    try:
        volcano_df['replacement_name'] = volcano_df['Protein_IDs'].apply(
            lambda x: x.split(';')[0])
        volcano_df.loc[volcano_df.Gene_names.isnull(),
                       'Gene_names'] = volcano_df.loc[volcano_df.Gene_names.isnull(), 'replacement_name']
        gene_name = volcano_df["Gene_names"]
        log_2_fc = volcano_df['log2FC']
        p_value = volcano_df['pvalue']

        return pd.DataFrame({"Gene Name": gene_name, "log2(Fold change)": log_2_fc, "P-value": p_value})
    except Exception:
        print("Error in {}".format(volcano_file))
        print("Columns: {}".format(volcano_df.columns))
        print(traceback.format_exc())
        exit(1)


def write_csv(df, filepath):
    df.to_csv(filepath, index=True, header=True)


def generate_csv_path(filepath, filename):
    dirname = os.path.dirname(filepath)
    return os.path.join(dirname, filename)


def generate_saint_csv_path(saint_xlsx_filepath):
    return generate_csv_path(saint_xlsx_filepath, "saint_score_web.csv")


def generate_volcano_csv_path(volcano_xlsx_filepath):
    return generate_csv_path(volcano_xlsx_filepath, "volcano_plot_web.csv")


def pregen_saint_files(directory):
    saint_files = find_all_saintscore_xlsx(directory)
    saint_dfs = map(generate_saint_df, saint_files)
    saint_csv_paths = map(generate_saint_csv_path, saint_files)
    for saint_df, saint_csv_path in zip(saint_dfs, saint_csv_paths):
        write_csv(saint_df, saint_csv_path)


def pregen_volcano_files(directory):
    volcano_files = find_all_volcanoplot_xlsx(directory)
    volcano_dfs = map(generate_volcano_df, volcano_files)
    volcano_csv_paths = map(generate_volcano_csv_path, volcano_files)
    for volcano_df, volcano_csv_path in zip(volcano_dfs, volcano_csv_paths):
        write_csv(volcano_df, volcano_csv_path)


def main(directory):
    pregen_saint_files(directory)
    pregen_volcano_files(directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pregen the saint files")
    parser.add_argument('directory', type=str,
                        help="will convert all files in directory recursively")
    args = parser.parse_args()
    main(args.directory)
