from gmsc_mapper.map_taxonomy import store_index,smorf_taxonomy,deep_lca
import pytest

from conftest import VERSION_COMMENT

known_mapped_taxonomy = ["smORF_0\t4\td__Bacteria",
                         "smORF_1\t3\tUnknown",
                         "smORF_2\t2\td__Bacteria;p__Firmicutes_A",
                         "smORF_2\t1\tUnknown",
                         "smORF_2\t0\td__Bacteria;p__Actinobacteriota;c__Actinomycetia;o__Actinomycetales;f__Microbacteriaceae;g__Microbacterium;s__Microbacterium sp003476465"]

def test_smorf_taxonomy(tmp_path):
    mapped_taxonomy = []
    index_tax_dict = store_index('./tests/test_taxonomy_index.tsv')
    taxonomy_file = smorf_taxonomy(index_tax_dict,'./tests/test_taxonomy.npy','./tests/alignment.tsv',str(tmp_path))
    with open(taxonomy_file,"rt") as f:
        for line in f:
            mapped_taxonomy.append(line.replace("\n",""))
    assert mapped_taxonomy == known_mapped_taxonomy

known_taxonomy = ["q_seqid\ttaxonomy","smORF_0\td__Bacteria","smORF_1\t","smORF_2\td__Bacteria"]

def test_deep_lca(tmp_path):
    deep_lca_taxonomy = []
    deep_lca('./tests/test_taxonomy_index.tsv',
             './tests/test_taxonomy.npy',
             str(tmp_path),
             './tests/alignment.tsv',
             str(tmp_path))
    with open(tmp_path / 'taxonomy.out.smorfs.tsv',"rt") as f:
        for line in f:
            if line.startswith('#'):
                assert line.strip() == VERSION_COMMENT
                continue
            deep_lca_taxonomy.append(line.replace("\n",""))
    assert deep_lca_taxonomy == known_taxonomy

if __name__ == '__main__':
    pytest.main()
