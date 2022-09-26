# GMSC-mapper

Command line tool to query the Global Microbial smORFs Catalog (GMSC)

## Installation
### Source
Clone GMSC-mapper repository

```bash
git clone https://github.com/BigDataBiology/GMSC-mapper.git
```

Create conda environment(only support python v3.8/v3.9)

```bash
conda create -n gmscmapper python=3.8
or
conda create -n gmscmapper python=3.9
```

You will need the following dependencies:

- [MMseqs2](https://github.com/soedinglab/MMseqs2)
- [Diamond](https://github.com/bbuchfink/diamond)

The easiest way to install the dependencies is with [conda](https://conda.io):

```bash
conda install -c conda-forge -c bioconda mmseqs2
conda install -c bioconda -c conda-forge diamond=2.0.13
```

Once the dependencies are installed, you can install GMSC-mapper by running:

```bash
cd GMSC-mapper
python setup.py install
```

## Example usage
### Default
1. Input is genome contig sequences.

```bash
python3 main.py -i example.fa -o output
```

2. Input is amino acid sequences.

```bash
python3 main.py --aa-genes example.faa -o output
```

3. Input is nucleotide gene sequences.

```bash
python3 main.py --nt-genes example.fna -o output
```

### GMSC database/habitat/taxonomy/quality file path can be assigned on your own after you download them.
```bash
python3 main.py -i example.fa -o output --db exampledb.dmnd
```
```bash
python3 main.py -i example.fa -o output --habitat ref_habitat.txt 
```
```bash
python3 main.py -i example.fa -o output --taxonomy ref_taxonomy.txt 
```
```bash
python3 main.py -i example.fa -o output --quality ref_quality.txt
```

### Habitat/taxonomy/quality annotation is optional
If you don't want to annotate habitat/taxonomy/quality you can use `--nohabitat`/`--notaxonomy`/`--noquality`.
```bash
python3 main.py -i example.fa -o output --nohabitat
```
```bash
python3 main.py -i example.fa -o output --notaxonomy
```
```bash
python3 main.py -i example.fa -o output --noquality
```
## Example Output
The output folder will contain
- Outputs of smORF prediction (Macrel).
- Complete mapping result table, listing all the hits in GMSC, per smORF (Default:Diamond/MMseqs).
- Habitat annotation of smORFs.(optional)
- Taxonomy annotation of smORFs.(optional)
- Quality annotation of smORFs.(optional)

## Parameters
* `-i/--input`: Path to the input genome contig sequence FASTA file (possibly .gz/.bz2/.xz compressed).

* `--aa-genes`: Path to the input amino acid sequence FASTA file (possibly .gz/.bz2/.xz compressed).

* `--nt-genes`: Path to the input nucleotide gene sequence FASTA file (possibly .gz/.bz2/.xz compressed).

* `--nofilter`: Use this if no need to filter <100aa input sequences.

* `-o/--output`: Output directory (will be created if non-existent).

* `--tool`: Sequence alignment tool(Diamond/MMseqs).

* `--db`: Path to the GMSC database file.

* `--id`: Minimum identity to report an alignment(range 0.0-1.0).

* `--cov`: Minimum coverage to report an alignment(range 0.0-1.0).

* `-e/--evalue`: Maximum e-value to report alignments(default=0.00001).

* `--outfmt`: Output format of alignment result.

(Diamond default is "6,qseqid,sseqid,full_qseq,full_sseq,qlen,slen,pident,length,evalue,qcovhsp,scovhsp".

MMseqs default is "query,target,qseq,tseq,qlen,tlen,fident,alnlen,evalue,qcov,tcov".

The first two column in result format of Diamond/MMseqs must be "qseqid"/"query" and "sseqid"/"target".)

* `--habitat`: Path to the habitat file.

* `--nohabitat`: Use this if no need to annotate habitat.

* `--taxonomy`: Path to the taxonomy file.

* `--notaxonomy`: Use this if no need to annotate taxonomy.

* `--quality`: Path to the quality file.

* `--noquality`: Use this if no need to annotate quality.

* `-t/--threads`: Number of CPU threads(default=3).