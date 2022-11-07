def mmseqs_contig_test():
    import filecmp

    predict_flag = filecmp.cmp("./tests/mmseqs_contig/predicted.filterd.smorf.faa", "./examples_output/predicted.filterd.smorf.faa")
    if not predict_flag:
        print('\nContig input of MMseqs2 mode predicted fasta results have something wrong.\n')

    fasta_flag = filecmp.cmp("./tests/mmseqs_contig/mapped.smorfs.faa", "./examples_output/mapped.smorfs.faa")
    if not fasta_flag:
        print('\nContig input of MMseqs2 mode mapped fasta results have something wrong.\n')

    habitat_flag = filecmp.cmp("./tests/mmseqs_contig/habitat.out.smorfs.tsv", "./examples_output/habitat.out.smorfs.tsv")
    if not habitat_flag:
        print('\nContig input of MMseqs2 mode habitat results have something wrong.\n')

    taxonomy_flag = filecmp.cmp("./tests/mmseqs_contig/taxonomy.out.smorfs.tsv", "./examples_output/taxonomy.out.smorfs.tsv")
    if not taxonomy_flag:
        print('\nContig input of MMseqs2 mode taxonomy results have something wrong.\n')

    quality_flag = filecmp.cmp("./tests/mmseqs_contig/quality.out.smorfs.tsv", "./examples_output/quality.out.smorfs.tsv")
    if not quality_flag:
        print('\nContig input of MMseqs2 mode quality results have something wrong.\n')

    summary_flag = filecmp.cmp("./tests/mmseqs_contig/summary.txt", "./examples_output/summary.txt")
    if not summary_flag:
        print('\nContig input of MMseqs2 mode summary results have something wrong.\n')

    if predict_flag and fasta_flag and habitat_flag and taxonomy_flag and quality_flag and summary_flag:
        print('\nContig input of MMseqs2 mode checking has passed.\n')

    return(predict_flag,fasta_flag,habitat_flag,taxonomy_flag,quality_flag,summary_flag)

mmseqs_contig_test()