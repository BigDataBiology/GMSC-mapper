import filecmp
import shutil
import sys
import pytest
import subprocess

from conftest import has_version_comment, read_text_without_version_comment, requires_binary

@requires_binary("mmseqs")
def test_mmseqs_contig(tmp_path):
    ok = True
    dbdir = str(tmp_path / "db")
    outdir = str(tmp_path / "output")
    shutil.copytree("./examples", dbdir)

    subprocess.check_call(['gmsc-mapper','createdb',
                          '-i','examples/target.faa',
                          '-o', dbdir,
                          '-m','mmseqs',
                          '--quiet'])

    subprocess.check_call(['gmsc-mapper',
                          '-i','examples/example.fa',
                          '-o', outdir,
                          '--dbdir', dbdir,
                          '--quiet',
                          '--tool','mmseqs'])

    versioned_outputs = {
        "habitat.out.smorfs.tsv",
        "taxonomy.out.smorfs.tsv",
        "quality.out.smorfs.tsv",
        "domain.out.smorfs.tsv",
        "summary.txt",
    }

    def checkf(f):
        if f in versioned_outputs:
            assert has_version_comment(f"{outdir}/{f}")
            return read_text_without_version_comment(f"./tests/mmseqs_contig/{f}") == \
                read_text_without_version_comment(f"{outdir}/{f}")
        return filecmp.cmp(f"./tests/mmseqs_contig/{f}",
                            f"{outdir}/{f}")

    if not checkf("predicted.filtered.smorf.faa"):
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
