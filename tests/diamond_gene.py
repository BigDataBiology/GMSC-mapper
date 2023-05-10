import filecmp
import sys

alignment_flag = filecmp.cmp("./tests/diamond_gene/alignment.out.smorfs.tsv", "./examples_output/alignment.out.smorfs.tsv")
ok = True
if not alignment_flag:
    ok = False
    print('\nGene input of Diamond mode alignment results have something wrong.\n')

fasta_flag = filecmp.cmp("./tests/diamond_gene/mapped.smorfs.faa", "./examples_output/mapped.smorfs.faa")
if not fasta_flag:
    ok = False
    print('\nGene input of Diamond mode mapped fasta results have something wrong.\n')

habitat_flag = filecmp.cmp("./tests/diamond_gene/habitat.out.smorfs.tsv", "./examples_output/habitat.out.smorfs.tsv")
if not habitat_flag:
    ok = False
    print('\nGene input of Diamond mode habitat results have something wrong.\n')

taxonomy_flag = filecmp.cmp("./tests/diamond_gene/taxonomy.out.smorfs.tsv", "./examples_output/taxonomy.out.smorfs.tsv")
if not taxonomy_flag:
    ok = False
    print('\nGene input of Diamond mode taxonomy results have something wrong.\n')

quality_flag = filecmp.cmp("./tests/diamond_gene/quality.out.smorfs.tsv", "./examples_output/quality.out.smorfs.tsv")
if not quality_flag:
    ok = False
    print('\nGene input of Diamond mode quality results have something wrong.\n')

summary_flag = filecmp.cmp("./tests/diamond_gene/summary.txt", "./examples_output/summary.txt")
if not summary_flag:
    ok = False
    print('\nGene input of Diamond mode summary results have something wrong.\n')

if ok:
    print('\nGene input of Diamond mode checking has passed.\n')
else:
    sys.exit(1)


