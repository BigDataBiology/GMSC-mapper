import sys
sys.path.append("..")
from gmsc_mapper.map_taxonomy import smorf_taxonomy,deep_lca
import pytest
import os

known_mapped_taxonomy = ["smORF_0\tGMSC10.90AA.000_257_823_465\td__Bacteria",
                         "smORF_1\tGMSC10.90AA.000_279_368_202\t",
                         "smORF_2\tGMSC10.90AA.000_276_471_764\td__Bacteria;p__Firmicutes_A",
                         "smORF_2\tGMSC10.90AA.000_265_853_435\t",
                         "smORF_2\tGMSC10.90AA.000_287_349_677\td__Bacteria;p__Actinobacteriota;c__Actinomycetia;o__Actinomycetales;f__Microbacteriaceae;g__Microbacterium;s__Microbacterium sp003476465"]
mapped_taxonomy = []
def test_smorf_taxonomy():
    taxonomy_file = smorf_taxonomy('./tests/test_taxonomy.txt','./tests/alignment.tsv',os.path.dirname(os.path.realpath(__file__)))
    with open(taxonomy_file,"rt") as f:
        for line in f:
            mapped_taxonomy.append(line.replace("\n",""))
    assert mapped_taxonomy == known_mapped_taxonomy

known_taxonomy = ["q_seqid\ttaxonomy","smORF_0\td__Bacteria","smORF_1\t","smORF_2\td__Bacteria"]
deep_lca_taxonomy = []
def test_deep_lca():
    deep_lca('./tests/test_taxonomy.txt',
             os.path.dirname(os.path.realpath(__file__)),
             './tests/alignment.tsv',
             os.path.dirname(os.path.realpath(__file__)))
    with open('./tests/taxonomy.out.smorfs.tsv',"rt") as f:
        for line in f:
            deep_lca_taxonomy.append(line.replace("\n",""))
    assert deep_lca_taxonomy == known_taxonomy
    
if __name__ == '__main__':
    pytest.main()
