from gmsc_mapper.translate import translate_nucleotide_fasta,check_frame
from gmsc_mapper.fasta import fasta_iter
import pytest

known_seq = {"ATGGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCTGCGGCATAA":"ATGGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCTGCGGCATAA",
             "GTGGCAGCGGCTGCGGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGTGGCGGTGGCTGTGGCGGCTGCGGCGACAGCGGCATGA":"ATGGCAGCGGCTGCGGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGTGGCGGTGGCTGTGGCGGCTGCGGCGACAGCGGCATGA",
             "TTAGCAGCAGCAGCACAT":"ATGTGCTGCTGCTGCTAA",
             "ATCGCAGCGGCTGCGGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGTGGCGGTGGCTGTGGCGGCTGCGGCGACAGCGGCATGA":"ATCGCAGCGGCTGCGGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGTGGCGGTGGCTGTGGCGGCTGCGGCGACAGCGGCATGA"}

known_translated = {"GMSC10.90AA.000_000_000_000":"MAAAAAAAAAAAAA*",
                    "GMSC10.90AA.000_000_000_001":"MAAAAAAAAAAAAAAAAAAAAAAAAAAVAVAVAAAATAA*",
                    "GMSC10.90AA.000_000_000_002":"MAAAAAAAAAAAAAAAAAAAAAAAAAQQSTLESTNAIYVYNNLNKKAVQL*",
                    "GMSC10.90AA.000_000_000_003":"MAAAAAAAAAAAAAAAAAAAAAAGGARGENFDENKIDAEREAGVDVQVDRGVLLLLLLILLLLLLLLLLLLVLVTLAVLPCPDKGGD*",
                    "GMSC10.90AA.000_000_000_004":"MAAAAAAAAAAAAAAAAAAAAAVVAAAVVVAAAVVAVVVVAAVVAVAGVVVAAVQLPAYKIIKS*"}

def test_check_frame():
    for key,value in known_seq.items():
        assert check_frame(key) == value

translate_dict = {}
def test_translate(tmp_path):
    translated_file = tmp_path / "translated.faa.gz"
    translated_file = translate_nucleotide_fasta("./tests/test.fna", str(translated_file))
    for h,seq in fasta_iter(translated_file,full_header=True):
        translate_dict[h] = seq
    assert translate_dict == known_translated

if __name__ == '__main__':
    pytest.main()
