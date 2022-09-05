import sys
sys.path.append("..")
from gmsc_mapper.map_habitat import smorf_habitat
import pytest
import os

known_habitat = {"qseqid":"habitat",
                 "smORF_0":"human gut",
                 "smORF_1":"marine,wastewater,water associated",
                 "smORF_2":"marine,soil,water associated"}
habitat_dict = {}
def test_habitat():
    smorf_habitat(os.path.dirname(os.path.realpath(__file__)),'./tests/test_habitat.txt','./tests/alignment.tsv')
    with open('./tests/habitat.out.smorfs.tsv',"rt") as f:
        for line in f:
            qseqid,habitat = line.strip().split("\t")
            habitat_dict[qseqid] = habitat
    assert habitat_dict == known_habitat

if __name__ == '__main__':
    pytest.main()