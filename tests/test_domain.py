from gmsc_mapper.map_domain import smorf_domain
import pytest
import os

known_domain = {"qseqid":"cdd",
                 "smORF_0":"197696",
                 "smORF_1":"",
                 "smORF_2":"198061,429147,429887"}
domain_dict={}
def test_smorf_domain():
    smorf_domain('./tests/test_domain.txt',os.path.dirname(os.path.realpath(__file__)),'./tests/alignment.tsv')
    with open('./tests/domain.out.smorfs.tsv',"rt") as f:
        for line in f:
            qseqid,domain = line.split("\t")
            domain_dict[qseqid] = domain.strip()
    assert domain_dict == known_domain

if __name__ == '__main__':
    pytest.main()