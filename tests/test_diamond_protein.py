import filecmp
import shutil
import sys
import subprocess
import pytest

from conftest import has_version_comment, read_text_without_version_comment, requires_binary

@requires_binary("diamond")
def test_diamond_protein(tmp_path):
    ok = True
    dbdir = str(tmp_path / "db")
    outdir = str(tmp_path / "output")
    shutil.copytree("./examples", dbdir)

    subprocess.check_call(['gmsc-mapper','createdb',
                          '-i','examples/target.faa',
                          '-o', dbdir,
                          '-m','diamond',
                          '--quiet'])

    subprocess.check_call(['gmsc-mapper',
                          '--aa-genes','examples/example.faa',
                          '-o', outdir,
                          '--dbdir', dbdir,
                          '--quiet'])

    versioned_outputs = {
        "alignment.out.smorfs.tsv",
        "habitat.out.smorfs.tsv",
        "taxonomy.out.smorfs.tsv",
        "quality.out.smorfs.tsv",
        "domain.out.smorfs.tsv",
        "summary.txt",
    }

    def checkf(f):
        if f in versioned_outputs:
            assert has_version_comment(f"{outdir}/{f}")
            return read_text_without_version_comment(f"./tests/diamond_protein/{f}") == \
                read_text_without_version_comment(f"{outdir}/{f}")
        return filecmp.cmp(f"./tests/diamond_protein/{f}",
                            f"{outdir}/{f}")

    if not checkf("alignment.out.smorfs.tsv"):
        ok = False
        print('\nProtein input of Diamond mode alignment results have something wrong.\n')

    if not checkf("mapped.smorfs.faa"):
        ok = False
        print('\nProtein input of Diamond mode mapped fasta results have something wrong.\n')

    if not checkf("habitat.out.smorfs.tsv"):
        ok = False
        print('\nProtein input of Diamond mode habitat results have something wrong.\n')

    if not checkf("taxonomy.out.smorfs.tsv"):
        ok = False
        print('\nProtein input of Diamond mode taxonomy results have something wrong.\n')

    if not checkf("quality.out.smorfs.tsv"):
        ok = False
        print('\nProtein input of Diamond mode quality results have something wrong.\n')

    if not checkf("domain.out.smorfs.tsv"):
        ok = False
        print('\nProtein input of Diamond mode domain results have something wrong.\n')

    if not checkf("summary.txt"):
        ok = False
        print('\nProtein input of Diamond mode summary results have something wrong.\n')

    assert ok

if __name__ == '__main__':
    pytest.main()
