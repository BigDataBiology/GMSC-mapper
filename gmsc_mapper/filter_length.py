message_error = '''GMSC-mapper Error: Input sequences are all more than 303nt or 100aa,which will be filtered.
Please check if your input consist of contigs, which should use -i not --nt-genes or --aa-genes as input.\n'''

def filter_length(queryfile, tmpdirname, N):
    import sys
    import gzip
    from os import path
    from .fasta import fasta_iter
    filtered_file = path.join(tmpdirname, "filtered.faa.gz")

    with gzip.open(filtered_file, 'wt',compresslevel=1) as of:
        all_longer_flag = True
        for ID, seq in fasta_iter(queryfile):
            if len(seq) < N:
                all_longer_flag = False
                of.write(f'>{ID}\n{seq}\n')

        if all_longer_flag:
            sys.stderr.write(message_error)
            sys.exit(1)
    return filtered_file
