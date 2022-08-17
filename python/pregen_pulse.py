import argparse
import glob
import os
import pandas

def glob_pattern(directory, pattern):
    return glob.glob(os.path.join(directory, pattern), recursive = True)

def find_all_volcano_csvs(directory):
    return sorted(glob_pattern(directory, '**/*VolcanoPlot*.csv'))

def find_all_intensity_csvs(directory):
    return sorted(glob_pattern(directory, '**/*Intensity*.csv'))

def validate_file_pairs(volcano_files, intensity_files):
    file_pairs = zip(volcano_files, intensity_files)
    for volcano_file, intensity_file in file_pairs:
        volcano_dir = os.path.dirname(saint_file)
        intensity_dir = os.path.dirname(intensity_file) 
        if volcano_dir != intensity_dir:
            print(volcano_dir, intensity_dir)
            return False
    return True

def main(directory):
    volcano_files = find_all_volcano_csvs(directory)
    intensity_files = find_all_intensity_csvs(directory)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pregen the pulse files")
    parser.add_argument('directory', type=str,
                        help="will convert all files in directory recursively")
    args = parser.parse_args()
    main(args.directory) 
