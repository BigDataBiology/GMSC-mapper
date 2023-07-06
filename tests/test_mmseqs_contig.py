import filecmp
import sys
import pytest
import subprocess

def checkf(f):
    return filecmp.cmp(f"./tests/mmseqs_contig/{f}",
                        f"./examples_output/{f}")

def test_mmseqs_contig():
    ok = True

    subprocess.check_call(['gmsc-mapper','createdb',
                          '-i','examples/target.faa',
                          '-o','examples/',
                          '-m','mmseqs',
                          '--quiet'])
    
    subprocess.check_call(['gmsc-mapper',
                          '-i','examples/example.fa',
                          '-o','examples_output/',
                          '--db','examples/mmseqs_targetdb',
                          '--habitat','examples/ref_habitat.npy',
                          '--habitat-index','examples/ref_habitat_index.tsv',
                          '--quality','examples/ref_quality.txt',
                          '--taxonomy','examples/ref_taxonomy.npy',
                          '--taxonomy-index','examples/ref_taxonomy_index.tsv',
                          '--domain','examples/ref_domain.txt','--quiet',
                          '--tool','mmseqs'])

    if not checkf("predicted.filterd.smorf.faa"):
        ok = False
        print('\nContig input of MMseqs2 mode predicted fasta results have something wrong.\n')

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

    assert ok

if __name__ == '__main__':
    pytest.main()