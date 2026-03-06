import filecmp
import shutil
import sys
import pytest
import subprocess

from conftest import requires_binary

@requires_binary("diamond")
def test_diamond_contig(tmp_path):
    ok = True
    dbdir = str(tmp_path / "db")
    outdir = str(tmp_path / "output")
    shutil.copytree("./examples", dbdir)

    subprocess.check_call(['gmsc-mapper','createdb',
                          '-i','./examples/target.faa',
                          '-o', dbdir,
                          '-m','diamond',
                          '--quiet'])

    subprocess.check_call(['gmsc-mapper',
                          '-i','./examples/example.fa',
                          '-o', outdir,
                          '--dbdir', dbdir,
                          '--quiet'])

    def checkf(f):
        return filecmp.cmp(f"./tests/diamond_contig/{f}",
                            f"{outdir}/{f}")

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
