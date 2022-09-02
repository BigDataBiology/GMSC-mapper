def check_frame(seq):
    from Bio.Seq import reverse_complement

    start_codons = {'ATG','GTG','TTG'}
    reverse_stops = {'TTA', 'CTA', 'TCA'}
    if (seq[0:3] not in start_codons) and (seq[0:3] in reverse_stops):
        seq = reverse_complement(seq)
    if seq[0:3] in start_codons:
        seq = f'ATG{seq[3:]}'
    return seq

def translate_gene(nt_input,tmpdirname):
    from .fasta import fasta_iter
    from Bio.Seq import Seq
    from os import path

    translated_file = path.join(tmpdirname,"translated.faa")
    with open(translated_file,'wt') as of:
        for ID,seq in fasta_iter(nt_input):
            seq = check_frame(seq)
            translated_seq = Seq(seq).translate()
            of.write(f'>{ID}\n{translated_seq}\n')
    return translated_file