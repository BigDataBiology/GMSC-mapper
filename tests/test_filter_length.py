from gmsc_mapper.filter_length import filter_length
import pytest
import os
import gzip

def test_filter_length(tmp_path):
    filtered_file = filter_length("./tests/test_filter_length.fna",str(tmp_path),303)
    with gzip.open(filtered_file,"rt") as f:
        assert len(f.readlines()) == 4
    filtered_file = filter_length("./tests/test_filter_length.faa",str(tmp_path),100)
    with gzip.open(filtered_file,"rt") as f:
        assert len(f.readlines()) == 6

if __name__ == '__main__':
    pytest.main()
