#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
import multiprocessing as mp
import logging

# Get arguments to determine the file that we are going to use

parser = argparse.ArgumentParser()
parser.add_argument('inputdirectory', help='directory containing directories with the files.')
args = parser.parse_args()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Context manager cd
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

# Get list of files
entries = os.listdir(args.inputdirectory)

# Function to run MEME on a protein sequence file
def meme(protein_pairs):
    output_dir = os.path.join(args.inputdirectory, f"classic_meme_{os.path.basename(protein_pairs)}")
    os.makedirs(output_dir, exist_ok=True)
    with cd(output_dir):
        cmd2 = f'meme {protein_pairs} -protein -oc . -nostatus -time 14400 -mod zoops -nmotifs 15 -minw 6 -maxw 50 -objfun classic -markov_order 0'
        mast_cmd = f'mast -mev 1 meme.html {protein_pairs}'
        try:
            subprocess.check_call(cmd2, shell=True)
            subprocess.check_call(mast_cmd, shell=True)
            logging.info(f"MEME and MAST run completed for {protein_pairs}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running MEME or MAST for {protein_pairs}: {e}")

if __name__ == "__main__":
    # Set the number of processes to be used in parallel
    num_processes = 15
    # Create full paths for protein sequence files
    protein_files = [os.path.join(args.inputdirectory, entry) for entry in entries if entry.endswith('.fa')]

    with mp.Pool(processes=num_processes) as pool:
        pool.map(meme, protein_files)
