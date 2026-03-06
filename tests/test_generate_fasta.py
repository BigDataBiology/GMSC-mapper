from gmsc_mapper.main import generate_fasta
from gmsc_mapper.fasta import fasta_iter
import pytest
import os

known_list = [">smORF_0","MVFVLLSEMYPTKVRGLAMSIAGFALWIGTYLIGQLTPWMLQNLTPAGTFFLFAVMCVPYMLIVWKLVPETTGKSLEEIERYWTRSEQ*",
              ">smORF_1","MTFSVAGINAQGTTVIEDAECVDVSYPNFYEQLQMLAGQ*",
              ">smORF_2","MDELTKMGARIQVDGRTAIITGVKLFTGADVSAPDLRAGAALVIAGLAADGYTTVSDIGYIYRGYEGFEKKIQNLGGDIQLVNSEKEIARFKLRIV*"]

def test_generate_fasta(tmp_path):
    fasta_list = []
    (fasta_file,ifsuccess) = generate_fasta(str(tmp_path),"./tests/test.faa","./tests/alignment.tsv")
    with open(fasta_file,"rt") as f:
        for line in f:
            fasta_list.append(line.strip())
    assert fasta_list == known_list

if __name__ == '__main__':
    pytest.main()
