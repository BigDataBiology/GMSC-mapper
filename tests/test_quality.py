import sys
sys.path.append("..")
from gmsc_mapper.map_quality import smorf_quality
import pytest
import os

known_quality = {"qseqid":"quality",
                 "smORF_0":"high quality",
                 "smORF_1":"low quality",
                 "smORF_2":"high quality"}
quality_dict={}
def test_smorf_quality():
    smorf_quality(os.path.dirname(os.path.realpath(__file__)),'./tests/test_quality.txt','./tests/alignment.tsv')
    with open('./tests/quality.out.smorfs.tsv',"rt") as f:
        for line in f:
            qseqid,quality = line.strip().split("\t")
            quality_dict[qseqid] = quality
    assert quality_dict == known_quality

if __name__ == '__main__':
    pytest.main()