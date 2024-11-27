"""
Script to extract all zip files from directory/subdirectories based on the provided input_dir path.
"""

import os
import gzip
import shutil
import argparse


def extract_zip(zip_file_in, out):
    if not zip_file_in.endswith('.gz'):
        print("Extension not supported", zip_file_in)
        return
    os.makedirs(out, exist_ok=True)
    with gzip.open(zip_file_in, 'rb') as f_in, open(os.path.join(out, os.path.split(zip_file_in)[-1].rstrip(".gz")),
                                                    'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


def traverse_and_extract(path, out="output"):
    for dir_ in os.listdir(path):
        path_ = os.path.join(path, dir_)
        if os.path.isfile(path_):
           extract_zip(path_, out)
        else:
            # for file in files:
            #     file_path = os.path.join(root, file)
            #     extract_zip(file_path, root)
            # for dir_ in dirs:
            traverse_and_extract(path_, os.path.join(out, dir_))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Python Zip Extractor",
                                     description="Script to extract zip files in nested directory structure.")
    parser.add_argument("-i", "--input_dir",
                        type=str,
                        required=True,
                        help="Directory path to read the zip files from")
    parser.add_argument("-o", "--output_dir",
                        default="output",
                        type=str,
                        required=True,
                        help="Output directory path to write the extracted zip files to.")

    args = parser.parse_args()
    traverse_and_extract(args.input_dir, args.output_dir)
