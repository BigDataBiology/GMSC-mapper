from gmsc_mapper.map_domain import smorf_domain
import pytest

from conftest import VERSION_COMMENT

known_domain = {"qseqid":"cdd",
                 "smORF_0":"197696",
                 "smORF_1":"",
                 "smORF_2":"198061,429147,429887"}

def test_smorf_domain(tmp_path):
    domain_dict={}
    smorf_domain('./tests/test_domain.txt',str(tmp_path),'./tests/alignment.tsv')
    with open(tmp_path / 'domain.out.smorfs.tsv',"rt") as f:
        for line in f:
            if line.startswith('#'):
                assert line.strip() == VERSION_COMMENT
                continue
            qseqid,domain = line.split("\t")
            domain_dict[qseqid] = domain.strip()
    assert domain_dict == known_domain

if __name__ == '__main__':
    pytest.main()
