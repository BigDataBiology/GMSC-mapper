def filter_length(queryfile,tmpdirname,N):
    import sys
    from os import path
    from .fasta import fasta_iter
    filtered_file = path.join(tmpdirname,"filtered.faa")

    with open(filtered_file,'wt') as of:
        all_longer_flag = 1
        longer_exist_flag = 0
        for ID,seq in fasta_iter(queryfile):
            if len(seq) < N:
                all_longer_flag = 0
                of.write(f'>{ID}\n{seq}\n')
            else:
                longer_exist_flag = 1
        if all_longer_flag:
            sys.stderr.write("Input sequences are all more than 300nt or 100aa,which will be filtered. 1.If you don't want to filter,please use --nofilter flag. 2.Please check if your input is contigs,which should use -i not --nt-genes or --aa-genes as input.")
            sys.exit(1)
        else:
            if longer_exist_flag:
                print("Warning:Input has seqences more than 300nt or 100aa,which will be filtered.If you don't want to filter,please use --nofilter flag.")
    return filtered_file