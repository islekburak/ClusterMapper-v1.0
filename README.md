# ClusterMapper v1.0

This program helps you to make 2D-array from the BLAST output which is taken by format of 7. On the other hand, the program uses only the human protein sequences which are retrieve from this BLAST output. Cluster Omega is used to make global alignment & hierachical clustering between these sequences by using the similarity scores.

## Getting Started

To use this program, you should install pip on your system.
To install pip3 on Ubuntu or Debian Linux, open a new Terminal window and enter:

```
> sudo apt-get install python3-pip
```
### Prerequisites

The modules below should be installed in your Python3. ClusterMapper checks whether they are installed or not. If not, it will install them automatically.

```
argparse
pandas
matplotlib.pyplot
seaborn
biopython
Bio.Align.Applications
```

> You should have a BLAST output (with the format of 7 - outfmt7) to use as an input.

> You should have a database file (.fasta format) to make analysis via ClusterMapper. Database file should contain
complete proteome sequences for all eukaryotes. You can download the sequences from:

[ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/]()

### Important Tip
You should download only ".fasta" files. Using regex may be easy to get all the files that have same pattern.

>("*[0-9].*fasta.gz")

After downloading all ".fasta" files; you should use the command below, to merge all of them in a (db) file via bash commandline.
```
> cat *.fasta > mydb.fasta
```
## Download

To use this program, you can download it using the command below: 


```
> wget https://github.com/islekburak/ClusterMapper-v1.0.git
```

You can check the instructions with -h or --help flag.
```
> python3 ClusterMapper.py -h
> python3 ClusterMapper.py --help
```

## Running the tests

Analysis using ClusterMapper gives you 6 different outputs:

>.dnd file
>>It is a dendrogram out from Cluster Omega and may be used for creating cladogram.

>.fasta file
>>It consists of only complete human proteome sequences retrieved from BLAST output.

>.matrix file
>>2D matrix file (obtained from the similarity scores of only human sequences) to make further analysis or plotting.

>_aligned.txt
>>Cluster Omega global alignment output.

>_clustermap.png
>>Represents hierarchical clustering results and visual map of it.

>_heatmap.png
>>Heatmap from Cluster Omega analysis.

## Built With

* [Python3 ](https://www.python.org/download/releases/3.0/)
## Authors

* **Burak Islek** - [Computational Genomics Laboratory - Adebali Lab.
](https://adebalilab.org/)

See also the list of [contributors](https://github.com/orgs/CompGenomeLab/people) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

This work is supported by European Molecular Biology Organization. [(EMBO)](https://www.embo.org/)
