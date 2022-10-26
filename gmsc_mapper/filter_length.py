message_error_all_long = '''GMSC-mapper Error: Input sequences are all more than 303nt or 100aa,
which will be filtered. There are some options:
1.If you don't want to filter, please use --nofilter flag.
2.Please check if your input consist of contigs, which should
use -i not --nt-genes or --aa-genes as input.
'''

message_error_longer='''GMSC-mapper Warning: Input has seqences more than 303nt or 100aa,
which will be filtered. If you don't want to filter,
please use --nofilter flag.
'''


def filter_length(queryfile, tmpdirname, N):
    import sys
    
    from os import path
    from .fasta import fasta_iter
    
    filtered_file = path.join(tmpdirname, "filtered.faa")

    with open(filtered_file, 'wt') as of:
        all_longer_flag = 1
        longer_exist_flag = 0
        
        for ID, seq in fasta_iter(queryfile):
            if len(seq) < N:
                all_longer_flag = 0
                of.write(f'>{ID}\n{seq}\n')
            else:
                longer_exist_flag = 1
        
        if all_longer_flag:
            sys.stderr.write(message_error_all_long)
            sys.exit(1)
        else:
            if longer_exist_flag:
                print(message_error_longer)
    
    return filtered_file
