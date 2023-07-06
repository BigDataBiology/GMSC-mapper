import filecmp
import sys

def checkf(f):
    return filecmp.cmp(f"./tests/diamond_contig/{f}",
                        f"./examples_output/{f}")

ok = True

if not checkf("predicted.filterd.smorf.faa"):
    ok = False
    print('\nContig input of Diamond mode predicted fasta results have something wrong.\n')

if not checkf("alignment.out.smorfs.tsv"):
    ok = False
    print('\nContig input of Diamond mode alignment results have something wrong.\n')

if not checkf("mapped.smorfs.faa"):
    ok = False
    print('\nContig input of Diamond mode mapped fasta results have something wrong.\n')

if not checkf("habitat.out.smorfs.tsv"):
    ok = False
    print('\nContig input of Diamond mode habitat results have something wrong.\n')

if not checkf("taxonomy.out.smorfs.tsv"):
    ok = False
    print('\nContig input of Diamond mode taxonomy results have something wrong.\n')

if not checkf("quality.out.smorfs.tsv"):
    ok = False
    print('\nContig input of Diamond mode quality results have something wrong.\n')

if not checkf("domain.out.smorfs.tsv"):
    ok = False
    print('\nContig input of Diamond mode domain results have something wrong.\n')

if not checkf("summary.txt"):
    ok = False
    print('\nContig input of Diamond mode summary results have something wrong.\n')

if ok:
    print('\nContig input of Diamond mode checking has passed.\n')
else:
    sys.exit(1)