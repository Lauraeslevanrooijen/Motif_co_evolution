import os
import subprocess

def alphafold(file):
    input_file = os.path.join(input_dir, file)
    output_file = os.path.join(output_dir, os.path.splitext(file)[0])

    if os.path.exists(output_file):
        print(f"Skipping {file} as output directory already exists.")
        return

    os.makedirs(output_file,exist_ok=True)

    command = f"colabfold_batch --templates --amber --use-gpu-relax --model-type alphafold2_multimer_v3 {input_file} {output_file}"
    subprocess.call(command, shell=True)

if __name__ == '__main__':
    input_dir = '/home/laurar/laurar2/Protein_motive_evo/ProteinMotif/Alphafold/Pearson'
    output_dir = '/home/laurar/laurar2/Protein_motive_evo/ProteinMotif/Alphafold/Pearson'

files = os.listdir(input_dir)

for file in files:
    if file.endswith('.fa'):
        alphafold(file)
