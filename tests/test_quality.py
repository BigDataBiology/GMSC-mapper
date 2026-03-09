from gmsc_mapper.map_quality import smorf_quality
import pytest

from conftest import VERSION_COMMENT

known_quality = {"qseqid":"quality",
                 "smORF_0":"high quality",
                 "smORF_1":"low quality",
                 "smORF_2":"high quality"}

def test_smorf_quality(tmp_path):
    quality_dict={}
    smorf_quality(str(tmp_path),'./tests/test_quality.txt','./tests/alignment.tsv')
    with open(tmp_path / 'quality.out.smorfs.tsv',"rt") as f:
        for line in f:
            if line.startswith('#'):
                assert line.strip() == VERSION_COMMENT
                continue
            qseqid,quality = line.strip().split("\t")
            quality_dict[qseqid] = quality
    assert quality_dict == known_quality

if __name__ == '__main__':
    pytest.main()
