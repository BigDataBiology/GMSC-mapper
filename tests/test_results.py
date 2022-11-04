import sys
sys.path.append("..")
from tests.diamond_contig import diamond_contig_test
from tests.diamond_protein import diamond_protein_test
from tests.diamond_gene import diamond_gene_test
from tests.mmseqs_contig import mmseqs_contig_test
import pytest
import subprocess

def test_diamond_contig():
    subprocess.check_call([
            'python','./gmsc_mapper/main.py',
            '-i','./examples/example.fa',
            '-o','./examples_output/',
            '--db','./examples/targetdb.dmnd',
            '--habitat','./examples/ref_habitat.txt',
            '--quality','./examples/ref_quality.txt',
            '--taxonomy','./examples/ref_taxonomy.txt']) 

    alignment_flag,predict_flag,fasta_flag,habitat_flag,taxonomy_flag,quality_flag,summary_flag = diamond_contig_test()

    assert alignment_flag == True
    assert predict_flag == True
    assert fasta_flag == True
    assert habitat_flag == True
    assert taxonomy_flag == True
    assert quality_flag == True
    assert summary_flag == True

def test_diamond_protein():
    subprocess.check_call([
            'python','./gmsc_mapper/main.py',
            '--aa-genes','./examples/example.faa',
            '-o','./examples_output/',
            '--db','./examples/targetdb.dmnd',
            '--habitat','./examples/ref_habitat.txt',
            '--quality','./examples/ref_quality.txt',
            '--taxonomy','./examples/ref_taxonomy.txt']) 

    alignment_flag,fasta_flag,habitat_flag,taxonomy_flag,quality_flag,summary_flag = diamond_protein_test()

    assert alignment_flag == True
    assert fasta_flag == True
    assert habitat_flag == True
    assert taxonomy_flag == True
    assert quality_flag == True
    assert summary_flag == True

def test_diamond_gene():
    subprocess.check_call([
            'python','./gmsc_mapper/main.py',
            '--nt-genes','./examples/example.fna',
            '-o','./examples_output/',
            '--db','./examples/targetdb.dmnd',
            '--habitat','./examples/ref_habitat.txt',
            '--quality','./examples/ref_quality.txt',
            '--taxonomy','./examples/ref_taxonomy.txt']) 

    alignment_flag,fasta_flag,habitat_flag,taxonomy_flag,quality_flag,summary_flag = diamond_gene_test()

    assert alignment_flag == True
    assert fasta_flag == True
    assert habitat_flag == True
    assert taxonomy_flag == True
    assert quality_flag == True
    assert summary_flag == True

def test_mmseqs_contig():
    subprocess.check_call([
            'python','./gmsc_mapper/main.py',
            '-i','./examples/example.fa',
            '-o','./examples_output/',
            '--db','./examples/targetdb',
            '--habitat','./examples/ref_habitat.txt',
            '--quality','./examples/ref_quality.txt',
            '--taxonomy','./examples/ref_taxonomy.txt',
            '--tool','mmseqs']) 

    predict_flag,fasta_flag,habitat_flag,taxonomy_flag,quality_flag,summary_flag = mmseqs_contig_test()

    assert predict_flag == True
    assert fasta_flag == True
    assert habitat_flag == True
    assert taxonomy_flag == True
    assert quality_flag == True
    assert summary_flag == True

if __name__ == '__main__':
    pytest.main()