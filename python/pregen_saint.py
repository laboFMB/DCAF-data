import argparse
import glob
import os
import pandas as pd
import numpy as np

def glob_pattern(directory, pattern):
    return glob.glob(os.path.join(directory, pattern), recursive = True)

def find_all_saintscore_csvs(directory):
    return sorted(glob_pattern(directory, '**/*SaintScore*.csv'))

def find_all_intensity_csvs(directory):
    return sorted(glob_pattern(directory, '**/*Intensity*.csv'))

def get_file_pairs(saint_files, intensity_files):
    file_pairs= {}
    for saint_file in saint_files:
        dirname = os.path.dirname(saint_file)
        file_pairs[dirname] = [saint_file]
    for intensity_file in intensity_files:
        dirname = os.path.dirname(intensity_file)
        file_pairs[dirname].append(intensity_file)
    return file_pairs 

def generate_saint_df(saint_file, intensity_file):
    saint_df = pd.read_csv(saint_file)
    intensity_df = pd.read_csv(intensity_file)

    bait = saint_df['Bait'].replace('^X', '', regex=True)
    prey_gene = saint_df['PreyGene'].str.upper()
    saint_score = saint_df['SaintScore']
    log_2_fc = np.log2(saint_df['FoldChange']).round(3) 

    return pd.DataFrame({"Bait": bait, "Prey Gene": prey_gene, "Saint Score":saint_score, "log2FC":log_2_fc})


def main(directory):
    saint_files = find_all_saintscore_csvs(directory)
    intensity_files = find_all_intensity_csvs(directory)
    file_pairs = get_file_pairs(saint_files, intensity_files)
    for saint_file, intensity_file in file_pairs.values():
        saint_df = generate_saint_df(saint_file, intensity_file)
        dirname = os.path.dirname(saint_file)
        filepath = os.path.join(dirname, "saint_score_web.csv")
        saint_df.to_csv(filepath, index=True, header=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pregen the saint files")
    parser.add_argument('directory', type=str,
                        help="will convert all files in directory recursively")
    args = parser.parse_args()
    main(args.directory)
