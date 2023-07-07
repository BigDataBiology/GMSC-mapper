import filecmp
import sys
import pytest
import subprocess

def checkf(f):
    return filecmp.cmp(f"./tests/diamond_contig/{f}",
                        f"./examples_output/{f}")

def test_diamond_contig():
    ok = True

    subprocess.check_call(['gmsc-mapper','createdb',
                          '-i','./examples/target.faa',
                          '-o','./examples/',
                          '-m','diamond',
                          '--quiet'])
    
    subprocess.check_call(['gmsc-mapper',
                          '-i','./examples/example.fa',
                          '-o','./examples_output/',
                          '--db','./examples/diamond_targetdb.dmnd',
                          '--habitat','./examples/ref_habitat.npy',
                          '--habitat-index','./examples/ref_habitat_index.tsv',
                          '--quality','./examples/ref_quality.txt',
                          '--taxonomy','./examples/ref_taxonomy.npy',
                          '--taxonomy-index','./examples/ref_taxonomy_index.tsv',
                          '--domain','./examples/ref_domain.txt','--quiet'])

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

    assert ok

if __name__ == '__main__':
    pytest.main()