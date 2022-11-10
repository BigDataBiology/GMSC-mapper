# GMSC-mapper

GMSC-mapper is a command line tool to query the Global Microbial smORFs Catalog (GMSC).

GMSC-mapper can be used to 
- Find query smORFs (&lt; 100aa) homologous to Global Microbial smORFs Catalog (GMSC) by alignment.
  - Support 3 types of input:
    - contigs (GMSC-mapper will predict smORFs from contigs first)
    - amino acid sequences
    - nucleotide gene sequences
- Annotate query/predicted smORFs with quality, habitat and taxonomy information constructed manually in detail.

## Installation

### Source
#### Installation path 1

Clone GMSC-mapper repository

```bash
git clone https://github.com/BigDataBiology/GMSC-mapper.git
```

Create conda environment(only support python v3.8-10)

```bash
conda create -n gmscmapper python=3.8
conda activate gmscmapper
or
conda create -n gmscmapper python=3.9
conda activate gmscmapper
```

You will need the following dependencies:

- [MMseqs2](https://github.com/soedinglab/MMseqs2)
- [Diamond](https://github.com/bbuchfink/diamond)

The easiest way to install the dependencies is with [conda](https://conda.io):

```bash
conda install -c conda-forge -c bioconda mmseqs2
conda install -c bioconda -c conda-forge diamond
```

Once the dependencies are installed, you can install GMSC-mapper by running:

```bash
cd GMSC-mapper
python setup.py install
```

#### Installation path 2
Clone GMSC-mapper repository and execute our installation script.

```bash
git clone https://github.com/BigDataBiology/GMSC-mapper.git
cd GMSC-mapper
./install.sh
```

It should create a conda environment (python v3.9) called **gmscmapper**
inserted in the folder `envs/` located in the GMSC-mapper main location.
To call this environment:

```bash
conda activate /path/to/GMSC-mapper/envs/gmscmapper
```

During the process, we install also the following dependencies:

- [MMseqs2](https://github.com/soedinglab/MMseqs2)
- [Diamond](https://github.com/bbuchfink/diamond)

### Example test
Because the whole GMSC database is large, and takes some minutes to process. 

If you want to check if the installation works well, you can test with mock datasets easily and fast.

- Create GMSC database index

Default alignment tool is Diamond.

```bash
gmsc-mapper createdb -i examples/target.faa -o examples/ -m diamond
```

If you want to use MMseqs2 as your alignment tool, you need to create GMSC database index in MMseqs2 format.

```bash
gmsc-mapper createdb -i examples/target.faa -o examples/ -m mmseqs
```

- Input is genome contig sequences.

```bash
gmsc-mapper -i ./examples/example.fa -o ./examples_output/ --db ./examples/targetdb.dmnd --habitat ./examples/ref_habitat.npy --habitat-index ./examples/ref_habitat_index.tsv --quality ./examples/ref_quality.txt --taxonomy ./examples/ref_taxonomy.npy --taxonomy-index ./examples/ref_taxonomy_index.tsv
```

- Input is amino acid sequences.

```bash
gmsc-mapper --aa-genes ./examples/example.faa -o ./examples_output/ --db ./examples/targetdb.dmnd --habitat ./examples/ref_habitat.npy --habitat-index ./examples/ref_habitat_index.tsv --quality ./examples/ref_quality.txt --taxonomy ./examples/ref_taxonomy.npy --taxonomy-index ./examples/ref_taxonomy_index.tsv
```

- Input is nucleotide gene sequences.

```bash
gmsc-mapper --nt-genes ./examples/example.fna -o ./examples_output/ --db ./examples/targetdb.dmnd --habitat ./examples/ref_habitat.npy --habitat-index ./examples/ref_habitat_index.tsv --quality ./examples/ref_quality.txt --taxonomy ./examples/ref_taxonomy.npy --taxonomy-index ./examples/ref_taxonomy_index.tsv
```

- Check another alignment tool: MMseqs2

```bash
gmsc-mapper -i ./examples/example.fa -o ./examples_output/ --db ./examples/targetdb --habitat ./examples/ref_habitat.npy --habitat-index ./examples/ref_habitat_index.tsv --quality ./examples/ref_quality.txt --taxonomy ./examples/ref_taxonomy.npy --taxonomy-index ./examples/ref_taxonomy_index.tsv --tool mmseqs
```

## Usage
Please make `GMSC-mapper/gmsc_mapper` as your work directory.

### Create GMSC database index
`-o`: Path to database output directory.(default: `GMSC-mapper/db`)

`-m`: Alignment tool (Diamond / MMseqs2).

```
cd gmsc_mapper
gmsc-mapper createdb -i ../db/90AA_GMSC.faa.gz -m diamond
```
or
```
cd gmsc_mapper
gmsc-mapper createdb -i ../db/90AA_GMSC.faa.gz -m mmseqs
```

### Default
GMSC database / habitat / taxonomy / quality file path and output directory path can be assigned on your own.Default is `GMSC-mapper/db` and `GMSC-mapper/output`.

1. Input is genome contig sequences.

```bash
gmsc-mapper -i ../examples/example.fa
```

2. Input is amino acid sequences.

```bash
gmsc-mapper --aa-genes ../examples/example.faa 
```

3. Input is nucleotide gene sequences.

```bash
gmsc-mapper --nt-genes ../examples/example.fna
```

### Alignment tool: Diamond / MMseqs2 is optional
If you want to change alignment tool (Diamond / MMseqs2), you can use `--tool`.

```bash
gmsc-mapper -i ../examples/example.fa --tool mmseqs
```

### Habitat / taxonomy / quality annotation is optional
If you don't want to annotate habitat / taxonomy / quality you can use `--nohabitat`/`--notaxonomy`/`--noquality`.

```bash
gmsc-mapper -i ../examples/example.fa --nohabitat --notaxonomy --noquality
```

## Output files
The output folder will contain

- Outputs of smORFs prediction (predicted.filterd.smorf.faa)

  A FASTA file with the sequences of the predicted smORFs. It is generated when the input file is contigs.

- Complete alignment result table (diamond.out.smorfs.tsv / mmseqs.out.smorfs.tsv)

  A file listing all the query hits of GMSC, from Diamond or MMseqs2.

  The file format is followed by a space-separated list of these keywords:

  `qseqid`: Query seq id

  `sseqid`: Target seq id (in GMSC)

  `full_qseq`: Query sequences

  `full_sseq`: Target sequences (in GMSC)

  `qlen`: Query sequences length

  `slen`: Target sequences length

  `length`: Alignment length

  `qstart`: Start of alignment in query

  `qend`: End of alignment in query

  `sstart`: Start of alignment in target

  `send`: End of alignment in target

  `bitscore`: Bit score

  `pident`: Percentage of identical matches

  `evalue`: Expect value

  `qcovhsp`: Query Coverage

  `scovhsp`: Target Coverage

- Total smORFs homologous to GMSC (mapped.smorfs.faa)

  A FASTA file with the sequences of query/predicted smORFs homologous to GMSC.

- Habitat annotation of smORFs (optional) (habitat.out.smorfs.tsv) 

  A file listing the habitat annotation for each smORF homologous to GMSC.

  There are two columns in the file:

  `qseqid`: Query seq id

  `habitat`: Habitat, ',' separated if the sequences is from multiple habitats

- Taxonomy annotation of smORFs (optional) (taxonomy.out.smorfs.tsv)

  A file listing the taxonomy annotation for each smORF homologous to GMSC.

  There are two columns in the file:

  `qseqid`: Query seq id

  `taxonomy`: Taxonomy, ';' separated between each taxonomy rank

- Quality annotation of smORFs (optional) (quality.out.smorfs.tsv)

  A file listing the quality annotation for each smORF homologous to GMSC.

  `qseqid`: Query seq id

  `quality`: Quality label

- Summry (summary.txt)

  A file providing a human-readable summary of the results.

## Parameters
* `-i/--input`: Path to the input genome contig sequence FASTA file (possibly .gz compressed).

* `--aa-genes`: Path to the input amino acid sequence FASTA file (possibly .gz compressed).

* `--nt-genes`: Path to the input nucleotide gene sequence FASTA file (possibly .gz compressed).

* `-o/--output`: Output directory (will be created if non-existent). (default: ../output)

* `--tool`: Sequence alignment tool (Diamond / MMseqs). (default: diamond)

*  `-s/--sensitivity`: Sensitivity. (default: --more-sensitive (Diamond) 5.7 (mmseqs))

* `--id`: Minimum identity to report an alignment (range 0.0-1.0). (default: 0.0)

* `--cov`: Minimum coverage to report an alignment (range 0.0-1.0). (default: 0.9)

* `-e/--evalue`: Maximum e-value to report alignments. (default: 1e-05)

* `-t/--threads`: Number of CPU threads. (default: 1)

* `--filter`: Use this to filter <100 aa or <303 nt input sequences. (default: False)

* `--nohabitat`: Use this if no need to annotate habitat. (default: False)

* `--notaxonomy`: Use this if no need to annotate taxonomy. (default: False)

* `--noquality`: Use this if no need to annotate quality. (default: False)

* `--quiet`: Disable alignment console output. (default:False)

### Subcommands and Parameters 
Subcommands: `gmsc-mapper createdb`

* `-i`: Path to the GMSC FASTA file.

* `-o/--output`: Path to database output directory. (default: ../db)

* `-m/--mode`: Alignment tool (Diamond / MMseqs2).

* `--quiet`: Disable alignment console output. (default:False)
