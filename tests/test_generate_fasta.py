from gmsc_mapper.main import generate_fasta
import pytest

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
    assert ifsuccess

def test_generate_fasta_missing_alignment(tmp_path):
    fasta_file, ifsuccess = generate_fasta(
        str(tmp_path), "./tests/test.faa", str(tmp_path / "missing.tsv")
    )
    assert fasta_file == ""
    assert not ifsuccess

def test_generate_fasta_empty_alignment(tmp_path):
    empty_alignment = tmp_path / "empty.tsv"
    empty_alignment.write_text("")

    fasta_file, ifsuccess = generate_fasta(
        str(tmp_path), "./tests/test.faa", str(empty_alignment)
    )
    assert fasta_file == ""
    assert not ifsuccess

if __name__ == '__main__':
    pytest.main()
