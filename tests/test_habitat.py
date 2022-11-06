import sys
sys.path.append("..")
from gmsc_mapper.map_habitat import smorf_habitat
import pytest
import os

known_habitat = {"qseqid":"habitat",
                 "smORF_0":"soil",
                 "smORF_1":"marine,water associated",
                 "smORF_2":"human gut,marine,soil,wastewater,water associated"}
habitat_dict = {}
def test_habitat():
    smorf_habitat('./tests/test_habitat_index.txt', os.path.dirname(os.path.realpath(__file__)), './tests/test_habitat.npy', './tests/alignment.tsv')
    with open('./tests/habitat.out.smorfs.tsv',"rt") as f:
        for line in f:
            qseqid,habitat = line.strip().split("\t")
            habitat_dict[qseqid] = habitat
    print(habitat_dict)
    assert habitat_dict == known_habitat

if __name__ == '__main__':
    pytest.main()