from gmsc_mapper.map_taxonomy import store_index,smorf_taxonomy,deep_lca
import pytest
import os

known_mapped_taxonomy = ["smORF_0\t4\td__Bacteria",
                         "smORF_1\t3\tUnknown",
                         "smORF_2\t2\td__Bacteria;p__Firmicutes_A",
                         "smORF_2\t1\tUnknown",
                         "smORF_2\t0\td__Bacteria;p__Actinobacteriota;c__Actinomycetia;o__Actinomycetales;f__Microbacteriaceae;g__Microbacterium;s__Microbacterium sp003476465"]
mapped_taxonomy = []
def test_smorf_taxonomy():
    index_tax_dict = store_index('./tests/test_taxonomy_index.tsv')
    taxonomy_file = smorf_taxonomy(index_tax_dict,'./tests/test_taxonomy.npy','./tests/alignment.tsv',os.path.dirname(os.path.realpath(__file__)))
    with open(taxonomy_file,"rt") as f:
        for line in f:
            mapped_taxonomy.append(line.replace("\n",""))
    assert mapped_taxonomy == known_mapped_taxonomy

known_taxonomy = ["q_seqid\ttaxonomy","smORF_0\td__Bacteria","smORF_1\t","smORF_2\td__Bacteria"]
deep_lca_taxonomy = []
def test_deep_lca():
    deep_lca('./tests/test_taxonomy_index.tsv',
             './tests/test_taxonomy.npy',
             os.path.dirname(os.path.realpath(__file__)),
             './tests/alignment.tsv',
             os.path.dirname(os.path.realpath(__file__)))
    with open('./tests/taxonomy.out.smorfs.tsv',"rt") as f:
        for line in f:
            deep_lca_taxonomy.append(line.replace("\n",""))
    assert deep_lca_taxonomy == known_taxonomy

if __name__ == '__main__':
    pytest.main()
