# GMSC-mapper

GMSC-mapper is a command line tool to query the Global Microbial smORFs Catalog (GMSC).

GMSC-mapper can be used to 
- Find query smORFs (&lt; 100aa) homologous to Global Microbial smORFs Catalogue (GMSC) by alignment.
  - Support 3 types of input:
    - contigs (GMSC-mapper will predict smORFs from contigs first)
    - amino acid sequences
    - nucleotide gene sequences
- Annotate query / predicted smORFs with quality, habitat and taxonomy information constructed manually in detail.

## Installation

Clone GMSC-mapper repository

```bash
git clone https://github.com/BigDataBiology/GMSC-mapper.git
```

Create conda environment

```bash
conda create -n gmscmapper python
conda activate gmscmapper
```

You will need the following dependencies:

- [MMseqs2](https://github.com/soedinglab/MMseqs2)
- [Diamond](https://github.com/bbuchfink/diamond)

The easiest way to install the dependencies is with [conda](https://conda.io):

```bash
conda install -c bioconda -c conda-forge mmseqs2
conda install -c bioconda -c conda-forge diamond=2.0.13
```

Once the dependencies are installed, you can install GMSC-mapper by running:

```bash
cd GMSC-mapper
python setup.py install
```

#### Example test
As the whole GMSC database is large and takes some minutes to process. To check if the installation works well, you can test with mock datasets easily and fast.

Please make `GMSC-mapper` as your work directory.

```bash
cd GMSC-mapper
```

- Create GMSC database index

Default alignment tool is DIAMOND.

```bash
gmsc-mapper createdb -i ./examples/target.faa -o ./examples/ -m diamond
```

- When input is genome contig sequences:

```bash
gmsc-mapper -i ./examples/example.fa -o ./examples_output/ --dbdir ./examples/ 
```

- When input is amino acid sequences:

```bash
gmsc-mapper --aa-genes ./examples/example.faa -o ./examples_output/ --dbdir ./examples/
```

- When input is nucleotide gene sequences:

```bash
gmsc-mapper --nt-genes ./examples/example.fna -o ./examples_output/ --dbdir ./examples/
```

- Check another alignment tool: MMseqs2

The default alignment tool is DIAMOND, if you want to use MMseqs2 as your alignment tool, you need to create GMSC database index in MMseqs2 format.

```bash
gmsc-mapper createdb -i ./examples/target.faa -o ./examples/ -m mmseqs
```

After index creation, you can specify tool as mmseqs and other usage is the same as above.

```bash
gmsc-mapper -i ./examples/example.fa -o ./examples_output/ --dbdir ./examples/ --tool mmseqs
```

## Usage

### Default usage

#### Download GMSC database and create index

We recommend to use `GMSC-mapper` as your current work directory. You can derectly follow the commonds below.

```bash
cd GMSC-mapper
```

Download GMSC database

```bash
gmsc-mapper downloaddb --dbdir ./db
```

The default `--dbdir` is `./db`. If you want to use custom `--dbdir` directory, it should be consistent with `-o` in the next creating database index step.

Create GMSC database index

```bash
gmsc-mapper createdb -i ./db/GMSC10.90AA.faa.gz -o ./db -m diamond
```

The input (`i`) is the fasta file (`GMSC10.90AA.faa.gz`) downloaded to the dbdir (default: `./db`) in the downloading step.

The default `-o` is `./db`. If you want to use custom `-o` directory, it should be consistent with `--dbdir` in the last downloading database step.

#### GMSC Annotation

GMSC Database directory (`--dbdir`) and output directory (`-o`) can be assigned on your own. Default is `./db` and `./output`. 

If you use `GMSC-mapper` as your current work directory. You can derectly follow the commonds below. Otherwise, you need to assign your custom `--dbdir` which contains database files.

```bash
cd GMSC-mapper
```

1. Input is genome contig sequences.

```bash
gmsc-mapper -i ./examples/example.fa --dbdir ./db
```

2. Input is amino acid sequences.

```bash
gmsc-mapper --aa-genes ./examples/example.faa --dbdir ./db
```

3. Input is nucleotide gene sequences.

```bash
gmsc-mapper --nt-genes ./examples/example.fna --dbdir ./db
```

### Further usage

#### Habitat / taxonomy / quality / domain annotation is optional

If you don't want to annotate habitat / taxonomy / quality you can use `--no-habitat`/`--no-taxonomy`/`--no-quality` / `--no-domain`.

```bash
gmsc-mapper -i ./examples/example.fa --dbdir ./db --no-habitat --no-taxonomy --no-quality --no-domain
```

#### Alignment tool: DIAMOND / MMseqs2 is optional

The default alignment tool is DIAMOND, if you want to use MMseqs2 as your alignment tool, you need to create GMSC database index in MMseqs2 format.

```bash
gmsc-mapper createdb -i ./db/GMSC10.90AA.faa.gz -o ./db -m mmseqs
```

Then you can assign`--tool` as mmseqs.

```bash
gmsc-mapper -i ./examples/example.fa --dbdir ./db --tool mmseqs
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

  This file lists the habitat annotations of the query/predicted sequence, where the habitat is obtained from the sequence annotations of its homologous origin in GMSC.

  There are two columns in the file:

  `qseqid`: Query seq id

  `habitat`: Habitat, ',' separated if the sequence is from multiple habitats

- Taxonomy annotation of smORFs (optional) (taxonomy.out.smorfs.tsv)

  This file lists the taxonomy annotations of the query/predicted sequence, where the taxonomy is obtained from the sequence annotations of its homologous origin in GMSC.

  There are two columns in the file:

  `qseqid`: Query seq id

  `taxonomy`: Taxonomy, ';' separated between each taxonomy rank

- Quality annotation of smORFs (optional) (quality.out.smorfs.tsv)

  This file lists the quality annotations of the query/predicted sequence, where the quality is obtained from the sequence annotations of its homologous origin in GMSC.

  `qseqid`: Query seq id

  `quality`: Quality label

- Conserved domain annotation of smORFs (optional) (domain.out.smorfs.tsv)

  This file lists the conservative domain annotations of the query/predicted sequence, where the conservative domain is obtained from the sequence annotations of its homologous origin in GMSC.

  `qseqid`: Query seq id

  `cdd`: Identifiers from Conserved domain database, ',' separated if the sequence is annotated with multiple conserved domains.

- Summary (summary.txt)

  A file providing a human-readable summary of the results.

## Parameters
* `-i/--input`: Path to the input genome contig sequence FASTA file (possibly .gz compressed).

* `--aa-genes`: Path to the input amino acid sequence FASTA file (possibly .gz compressed).

* `--nt-genes`: Path to the input nucleotide gene sequence FASTA file (possibly .gz compressed).

* `--dbdir`: Path to the GMSC database directory. (default: `./db`)

* `-o/--output`: Output directory (will be created if non-existent). (default: `./output`)

* `--tool`: Sequence alignment tool (Diamond / MMseqs). (default: diamond)

*  `-s/--sensitivity`: Sensitivity. (default: --more-sensitive (Diamond) 5.7 (mmseqs))

* `--id`: Minimum identity to report an alignment (range 0.0-1.0). (default: 0.0)

* `--cov`: Minimum coverage to report an alignment (range 0.0-1.0). (default: 0.9)

* `-e/--evalue`: Maximum e-value to report alignments. (default: 1e-05)

* `-t/--threads`: Number of CPU threads. (default: 1)

* `--filter`: Use this to filter <100 aa or <303 nt input sequences. (default: False)

* `--no-habitat`: Use this if no need to annotate habitat. (default: False)

* `--no-taxonomy`: Use this if no need to annotate taxonomy. (default: False)

* `--no-quality`: Use this if no need to annotate quality. (default: False)

* `--no-domain`: Use this if no need to annotate conserved domain. (default: False)

* `--quiet`: Disable alignment console output. (default:False)

### Subcommands and Parameters 
#### Download GMSC database annotation index files
Subcommands: `gmsc-mapper downloaddb`

* `--dbdir`: Path to GMSC database annotation index files. (default: `./db`. If `GMSC-mapper` is your current work directory, the database files will be downloaded at `GMSC-mapper/db`)

* `--all`: Download all database

* `-f`: Force download even if the files exist

#### Create database index of Diamond and mmseqs
Subcommands: `gmsc-mapper createdb`

* `-i`: Path to the GMSC FASTA file.

* `-o/--output`: Path to database index output of Diamond and MMseqs2. (default: `./db`. If `GMSC-mapper` is your current work directory, the database files will be created at `GMSC-mapper/db`)

* `-m/--mode`: Alignment tool (Diamond / MMseqs2).

* `--quiet`: Disable alignment console output. (default:False)
