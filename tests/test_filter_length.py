import sys
sys.path.append("..")
from gmsc_mapper.filter_length import filter_length
import pytest
import os
import gzip

def test_filter_length():
    filtered_file = filter_length("./tests/test_filter_length.fna",os.path.dirname(os.path.realpath(__file__)),303)
    with gzip.open(filtered_file,"rt") as f:
        assert len(f.readlines()) == 4
    filtered_file = filter_length("./tests/test_filter_length.faa",os.path.dirname(os.path.realpath(__file__)),100)
    with gzip.open(filtered_file,"rt") as f:
        assert len(f.readlines()) == 6  

if __name__ == '__main__':
    pytest.main()