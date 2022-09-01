import sys
sys.path.append("..")
from gmsc_mapper.main import uncompress
import pytest
import tempfile

def test_gz():
    true_list = []
    gz_list = []
    with open('test.fa','rt') as true_file:
        for line in true_file:
            true_list.append(line)
    with tempfile.TemporaryDirectory() as tmpdir:
        file = uncompress('test.fa.gz',tmpdir)
        with open(file,'rt') as gz_file:
            for line in gz_file:
                gz_list.append(line)
    assert true_list == gz_list

def test_xz():
    true_list = []
    xz_list = []
    with open('test.fa','rt') as true_file:
        for line in true_file:
            true_list.append(line)
    with tempfile.TemporaryDirectory() as tmpdir:
        file = uncompress('test.fa.xz',tmpdir)
        with open(file,'rt') as xz_file:
            for line in xz_file:
                xz_list.append(line)
    assert true_list == xz_list

def test_bzip():
    true_list = []
    bzip_list = []
    with open('test.fa','rt') as true_file:
        for line in true_file:
            true_list.append(line)
    with tempfile.TemporaryDirectory() as tmpdir:
        file = uncompress('test.fa.bz2',tmpdir)
        with open(file,'rt') as bzip_file:
            for line in bzip_file:
                bzip_list.append(line)
    assert true_list == bzip_list

if __name__ == '__main__':
    pytest.main()