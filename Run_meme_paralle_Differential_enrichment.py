#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
import multiprocessing as mp

# Get arguments to detemine the file that we are going to usage

parser = argparse.ArgumentParser()
parser.add_argument('inputdirectory', help='dicrectory containting directorys with the files.')
args = parser.parse_args()

#contexmanager cd
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
# get list of files

entries = os.listdir(args.inputdirectory)


# check for every
def meme(protein_pairs):
    with cd(args.inputdirectory+protein_pairs):
        cmd ='meme target.fa -protein -oc . -nostatus -time 17945 -mod zoops -p 2 -nmotifs 10 -minw 6 -maxw 50 -objfun de -markov_order 0 -neg control.fa'
        mast_cmd = f'mast -mev 1 meme.html {protein_pairs}.fa'
        subprocess.call(cmd, shell=True)
        subprocess.call(mast_cmd, shell=True)
        print(protein_pairs)
with mp.Pool(processes=15) as pool:
            pool.map(meme, entries)
