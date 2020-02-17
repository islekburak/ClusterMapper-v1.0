#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author @islekburak

import pip
def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(["install", package])

import_or_install("argparse")
import_or_install("pandas")
import_or_install("matplotlib.pyplot")
import_or_install("seaborn")
import_or_install("Bio.Align.Applications")

#libraries
import os
import argparse, textwrap
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from Bio.Align.Applications import ClustalOmegaCommandline

#details about program

#parse arguments
parser=argparse.ArgumentParser(prog="ClusterMapper.py",
	usage="python3 %(prog)s [options] <path_of_file>",
	description=textwrap.dedent("""\
		author:		islekbro @ adebalilab

		contact:	islekburak@sabanciuniv.edu"""),

	add_help=True,
	formatter_class=argparse.RawTextHelpFormatter, 
	epilog=textwrap.dedent("""\

#To use this program, you should install pip on your system. To install
pip3 on Ubuntu or Debian Linux, open a new Terminal window and enter:

# sudo apt-get install python3-pip

-----------------------------------------------------------------------------

This program helps you to make 2D-array from the BLAST output which is
taken by format of 7. On the other hand, the program uses only the human
protein sequences which are retrieve from this BLAST output. Cluster Omega
is used to make global alignment & hierachical clustering between these
sequences by using the similarity scores. Analysis using ClusterMapper.py
gives you 6 different outputs:

1).dnd file 		=>	It is a dendrogram out from Cluster Omega
				and may be used for creating cladogram.

2).fasta file 		=>	It consists of only complete human proteome
				sequences retrieved from BLAST output

3).matrix file 		=>	2D matrix file (obtained from the similarity
				scores of only human sequences) to make further
				analysis or plotting

4)_aligned.txt 		=>	Cluster Omega global alignment output

5)_clustermap.png 	=>	Represents hierarchical clustering results and
				visual map of it

6)_heatmap.png 		=>	Heatmap from Cluster Omega analysis

-----------------------------------------------------------------------------

To use this program you need some files:

> With "-i" flag, you can specify your first input. It should be a BLAST
output (in outfmt7).

> with "-db" flag you can specify your second input. It should contains
complete proteome sequences for all eukaryotes. You can download them
from;

ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/

You should download only ".fasta" files, with regex ("*[0-9].*fasta.gz").
After downloading all .fasta files; you should use the command below,
to merge all of them in a (db) file via using bash commandline.

(i.e) cat *.fasta > mydb.fasta

-----------------------------------------------------------------------------

"""))
parser.add_argument("-i","--input", metavar="<FASTA FILE>", required=True, help="Write the path of your input -output of BLAST- file (i.e. /home/Desktop/input.fasta)")
parser.add_argument("-od","--outdir", metavar="<DIRECTORY>", required=True, help="Write only the path where you want to put out/s (i.e. /home/Desktop/)")
parser.add_argument("-o","--outname", metavar="<OUTNAME>", help="Write the name of your output file/s (i.e. ABC)")
parser.add_argument("-db","--database", metavar="<DATABASE>", required=True, help="Write the path of your database -fasta- file (i.e. /home/Desktop/mydb.fasta)")

args=parser.parse_args()

#getting directory
directory = args.outdir

#getting input path
file_path=args.input

#assign outputs' names
name=args.outname

#reading file
a=pd.read_csv(file_path)
print("Blast output is reading...")

#finding all human hits and indexes
b=a[a["subject_id"].str.contains("HUMAN")==True]

#create lists with hit ranks and subject ids
subjectlist=b.subject_id.tolist()

mergedsubjects=[] 
for i in subjectlist: 
    if i not in mergedsubjects: 
        mergedsubjects.append(i)

print("All human sequences are collecting...")
#ask for database of fasta
path=args.database
#retrieving complete sequences from database that match with the subjects
infile=path
outfile=directory+"/"+"".join(name)+".fasta"
outfile = open (outfile, "w")

found=False
with open (path, "r") as myfasta:
	for line in myfasta:
		if ">" in line and not found:
			for item in mergedsubjects:
				if str(item) in line:
					outfile.write(line)
					found=True
					break
		elif ">" in line and found:
			for item in mergedsubjects:
				if str(item) in line:
					outfile.write(line)
					found=True
					break
				else:
					found=False
		elif ">" not in line and found:
			outfile.write(line)
outfile.close()

outfile=directory+"/"+name+".fasta"

print("All sequences are writing into new file...")
#using fasta sequences for MSA (clustalo-globalalignment)
in_file = outfile
out_file = directory+"/"+"".join(name)+"_aligned.txt"
mat_file = directory+"/"+"".join(name)+".mat"
dnd_file = directory+"/"+"".join(name)+".dnd"

#clustalo -i x.fasta --distmat-out=x.mat --guidetree-out=x.dnd -o x.aln --outfmt=clustal -v --full
clustalomega_cline = ClustalOmegaCommandline(infile=in_file, distmat_out=mat_file, guidetree_out=dnd_file, outfile=out_file, outfmt="clustal", verbose=True, distmat_full=True)

#print(clustalomega_cline)
clustalomega_cline()

print("Global alignment is running...")

infile=open(mat_file,"r")
out=open(directory+"/"+name+".matrix","w")

next(infile)
for i in infile:
	first=i.split()[0].split("|")[2].split("_")[0]
	others=i.split()[1:]
	string= ",".join(others)
	string2=first+","+string
	out.write(string2+"\n")
out.close()

os.remove(mat_file)
print("Matrix file has created.")
df=pd.read_csv(directory+"/"+name+".matrix", header=None)

headers=df.iloc[:,0].tolist()

df2=df.set_index(list(df)[0])
df2.columns=[i for i in headers]
df2.to_csv(directory+"/"+name+".matrix")


#using matrix file for create heatmap
df=pd.read_csv(directory+"/"+name+".matrix")
df=df.set_index("0")
del df.index.name

sns.heatmap(df, cmap="viridis")
plt.savefig(directory+"/"+name+"_heatmap.png")
plt.close()
print("Heatmap analysis has done.")

sns.clustermap(df, method="average", metric="euclidean", standard_scale=1, cmap="Spectral" , figsize=(10,10))
plt.savefig(directory+"/"+name+"_clustermap.png")
plt.close()
print("Cluster analysis has done.")
print("Thanks for using ClusterMapper:)")