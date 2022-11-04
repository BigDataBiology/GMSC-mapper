def diamond_contig_test():
    import filecmp

    alignment_flag = filecmp.cmp("./tests/diamond_contig/alignment.out.smorfs.tsv", "./examples_output/alignment.out.smorfs.tsv")
    if not alignment_flag:
        print('Contig input of Diamond mode alignment results have something wrong.')

    predict_flag = filecmp.cmp("./tests/diamond_contig/predicted.filterd.smorf.faa", "./examples_output/predicted.filterd.smorf.faa")
    if not predict_flag:
        print('Contig input of Diamond mode predicted fasta results have something wrong.')

    fasta_flag = filecmp.cmp("./tests/diamond_contig/mapped.smorfs.faa", "./examples_output/mapped.smorfs.faa")
    if not fasta_flag:
        print('Contig input of Diamond mode mapped fasta results have something wrong.')

    habitat_flag = filecmp.cmp("./tests/diamond_contig/habitat.out.smorfs.tsv", "./examples_output/habitat.out.smorfs.tsv")
    if not habitat_flag:
        print('Contig input of Diamond mode habitat results have something wrong.')

    taxonomy_flag = filecmp.cmp("./tests/diamond_contig/taxonomy.out.smorfs.tsv", "./examples_output/taxonomy.out.smorfs.tsv")
    if not taxonomy_flag:
        print('Contig input of Diamond mode taxonomy results have something wrong.')

    quality_flag = filecmp.cmp("./tests/diamond_contig/quality.out.smorfs.tsv", "./examples_output/quality.out.smorfs.tsv")
    if not quality_flag:
        print('Contig input of Diamond mode quality results have something wrong.')

    summary_flag = filecmp.cmp("./tests/diamond_contig/summary.txt", "./examples_output/summary.txt")
    if not summary_flag:
        print('Contig input of Diamond mode summary results have something wrong.')

    if alignment_flag and predict_flag and fasta_flag and habitat_flag and taxonomy_flag and quality_flag and summary_flag:
        print('Contig input of Diamond mode checking has passed')

    return(alignment_flag,predict_flag,fasta_flag,habitat_flag,taxonomy_flag,quality_flag,summary_flag)

diamond_contig_test()