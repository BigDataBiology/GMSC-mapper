# GMSC-mapper

GMSC-mapper is a command line tool to query the Global Microbial smORFs Catalog (GMSC).

GMSC-mapper can be used to 
- Find query smORFs (< 100aa) homologous to Global Microbial smORFs Catalog (GMSC) by alignment.
  - Support 3 types of input:
    - contigs (GMSC-mapper will predict smORFs from contigs first)
    - amino acid sequences
    - nucleotide gene sequences
- Annotate query/predicted smORFs with quality, habitat and taxonomy information constructed manually in detail.

## Installation

### Source

Clone GMSC-mapper repository and execute our installation script.

```bash
git clone https://github.com/BigDataBiology/GMSC-mapper.git
cd GMSC-mapper
./install.sh
```

It should create a conda environment (python vv3.9) called **gmscmapper**
inserted in the folder `envs/` located in the GMSC-mapper main location.
To call this environment:

```bash
conda activate /path/to/GMSC-mapper/envs/gmscmapper
```

During the process, we install also the following dependencies:

- [MMseqs2](https://github.com/soedinglab/MMseqs2)
- [Diamond](https://github.com/bbuchfink/diamond)

Because the whole GMSC database is large, and takes some time to process all the things. We perform a series of tests using mock datasets to check if the installation works well:

- test.sh

0. Create GMSC database index
`-o`: Path to database output directory.(default: `GMSC-mapper/examples`)

`-m`: Alignment tool (Diamond / MMseqs2).
```
cd gmsc_mapper
gmsc-mapper createdb -i ../examples/target.faa -o ../examples -m diamond
```
or
```
cd gmsc_mapper
gmsc-mapper createdb -i ../examples/target.faa -o ../examples -m mmseqs
```

1. Input is genome contig sequences.

```bash
gmsc-mapper -i ../examples/example.fa --db ../examples/targetdb.dmnd --habitat ../examples/ref_habitat.txt --quality ../examples/ref_quality.txt --taxonomy ../examples/ref_taxonomy.txt
```

2. Input is amino acid sequences.

```bash
gmsc-mapper --aa-genes ../examples/example.faa --db ../examples/targetdb.dmnd --habitat ../examples/ref_habitat.txt --quality ../examples/ref_quality.txt --taxonomy ../examples/ref_taxonomy.txt
```

3. Input is nucleotide gene sequences.

```bash
gmsc-mapper --nt-genes ../examples/example.fna --db ../examples/targetdb.dmnd --habitat ../examples/ref_habitat.txt --quality ../examples/ref_quality.txt --taxonomy ../examples/ref_taxonomy.txt
```

4. Check the Alignment tool: Diamond / MMseqs2 is optional

```bash
gmsc-mapper -i ../examples/example.fa --db ../examples/targetdb --habitat ../examples/ref_habitat.txt --quality ../examples/ref_quality.txt --taxonomy ../examples/ref_taxonomy.txt --tool mmseqs

gmsc-mapper -i ../examples/example.fa --db ../examples/targetdb --habitat ../examples/ref_habitat.txt --quality ../examples/ref_quality.txt --taxonomy ../examples/ref_taxonomy.txt --tool diamond
```

5. Flags to disable results from Habitat / taxonomy / quality annotation

```bash
gmsc-mapper -i ../examples/example.fa --db ../examples/targetdb.dmnd --habitat ../examples/ref_habitat.txt --quality ../examples/ref_quality.txt --taxonomy ../examples/ref_taxonomy.txt --nohabitat --notaxonomy --noquality
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

  `(qstart)`: Start of alignment in query

  `(qend)`: End of alignment in query

  `(sstart)`: Start of alignment in target

  `(send)`: End of alignment in target

  `(bitscore)`: Bit score

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

* `--filter`: Use this to filter < 100 aa / <303nt input sequences. (default: False)

* `-o/--output`: Output directory (will be created if non-existent). (default: ../output)

* `--tool`: Sequence alignment tool (Diamond / MMseqs). (default: diamond)

* `--db`: Path to the GMSC database file. (default: ../db/targetdb.dmnd)

*  `-s/--sensitivity`: Sensitivity. (default: --more-sensitive(Diamond) 5.7(mmseqs))

* `--id`: Minimum identity to report an alignment(range 0.0-1.0). (default: 0.0)

* `--cov`: Minimum coverage to report an alignment(range 0.0-1.0). (default: 0.9)

* `-e/--evalue`: Maximum e-value to report alignments(default=0.00001). (default: 1e-05)

* `--habitat`: Path to the habitat file. (default: ../db/ref_habitat.tsv.xz)

* `--nohabitat`: Use this if no need to annotate habitat. (default: False)

* `--taxonomy`: Path to the taxonomy file. (default: ../db/ref_taxonomy.tsv.xz)

* `--notaxonomy`: Use this if no need to annotate taxonomy. (default: False)

* `--quality`: Path to the quality file. (default: ../db/ref_quality.tsv.xz)

* `--noquality`: Use this if no need to annotate quality. (default: False)

* `-t/--threads`: Number of CPU threads. (default: 1)

### Subcommands and Parameters 
Subcommands: `gmsc-mapper createdb`

* `-i`: Path to the GMSC 90AA FASTA file.

* `-o/--output`: Path to database output directory. (default: ../db)

* `-m/--mode`: Alignment tool (Diamond / MMseqs2).

## Sensitivity choices considering time and memory usage
To be done