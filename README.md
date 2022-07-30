# GMSC-mapper

Command line tool to query the Global Microbial smORFs Catalog (GMSC)

## Installation

## Example usage
### Default
1. Input is genome contig sequences.

```bash
python3 main.py -i example.fa -o output
```

2. Input is protein sequences

```bash
python3 main.py --aa-genes example.faa -o output
```

### GMSC database/habitat/taxonomy/quality file path can be assigned on your own
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

* `-o/--output`: Output directory (will be created if non-existent).

* `--tool`: Sequence alignment tool(Diamond/MMseqs).

* `--db`: Path to the GMSC database file.

* `--id`: Minimum identity to report an alignment(range 0.0-1.0).

* `--cov`: Minimum coverage to report an alignment(range 0.0-1.0).

* `-e/--evalue`: Maximum e-value to report alignments(default=0.00001).

* `--habitat`: Path to the habitat file.

* `--nohabitat`: Use this if no need to annotate habitat.

* `--taxonomy`: Path to the taxonomy file.

* `--notaxonomy`: Use this if no need to annotate taxonomy.

* `--quality`: Path to the quality file.

* `--noquality`: Use this if no need to annotate quality.

* `-t/--threads`: Number of CPU threads(default=3).


