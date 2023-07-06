import filecmp
import sys

def checkf(f):
    return filecmp.cmp(f"./tests/mmseqs_contig/{f}",
                        f"./examples_output/{f}")

ok = True

if not checkf("predicted.filterd.smorf.faa"):
    ok = False
    print('\nContig input of MMseqs2 mode predicted fasta results have something wrong.\n')

if not checkf("alignment.out.smorfs.tsv"):
    ok = False
    print('\nContig input of MMseqs2 mode alignment results have something wrong.\n')

if not checkf("mapped.smorfs.faa"):
    ok = False
    print('\nContig input of MMseqs2 mode mapped fasta results have something wrong.\n')

if not checkf("habitat.out.smorfs.tsv"):
    ok = False
    print('\nContig input of MMseqs2 mode habitat results have something wrong.\n')

if not checkf("taxonomy.out.smorfs.tsv"):
    ok = False
    print('\nContig input of MMseqs2 mode taxonomy results have something wrong.\n')

if not checkf("quality.out.smorfs.tsv"):
    ok = False
    print('\nContig input of MMseqs2 mode quality results have something wrong.\n')

if not checkf("domain.out.smorfs.tsv"):
    ok = False
    print('\nContig input of MMseqs2 mode domain results have something wrong.\n')

if not checkf("summary.txt"):
    ok = False
    print('\nContig input of MMseqs2 mode summary results have something wrong.\n')

if ok:
    print('\nContig input of Diamond mode checking has passed.\n')
else:
    sys.exit(1)