import sys
sys.path.append("..")
from gmsc_mapper.filter_length import filter_length
from gmsc_mapper.fasta import fasta_iter
import pytest
import os

def test_filter_length():
    filtered_file = filter_length("test_filter_length.fna",os.path.dirname(os.path.realpath(__file__)),303)
    with open(filtered_file,"rt") as f:
        assert len(f.readlines()) == 4
    filtered_file = filter_length("test_filter_length.faa",os.path.dirname(os.path.realpath(__file__)),100)
    with open(filtered_file,"rt") as f:
        assert len(f.readlines()) == 6  

if __name__ == '__main__':
    pytest.main()