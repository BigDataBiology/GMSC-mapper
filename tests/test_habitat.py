from gmsc_mapper.map_habitat import smorf_habitat
import pytest
import os

known_habitat = {"qseqid":"habitat",
                 "smORF_0":"soil",
                 "smORF_1":"marine,water associated",
                 "smORF_2":"human gut,marine,soil,wastewater,water associated"}

def test_habitat(tmp_path):
    habitat_dict = {}
    smorf_habitat('./tests/test_habitat_index.txt', str(tmp_path), './tests/test_habitat.npy', './tests/alignment.tsv')
    with open(tmp_path / 'habitat.out.smorfs.tsv',"rt") as f:
        for line in f:
            qseqid,habitat = line.strip().split("\t")
            habitat_dict[qseqid] = habitat
    assert habitat_dict == known_habitat

if __name__ == '__main__':
    pytest.main()
