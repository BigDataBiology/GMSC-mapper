def diamond_gene_test():
    import filecmp

    alignment_flag = filecmp.cmp("./tests/diamond_gene/alignment.out.smorfs.tsv", "./examples_output/alignment.out.smorfs.tsv")
    if not alignment_flag:
        print('Gene input of Diamond mode alignment results have something wrong.')

    fasta_flag = filecmp.cmp("./tests/diamond_gene/mapped.smorfs.faa", "./examples_output/mapped.smorfs.faa")
    if not fasta_flag:
        print('Gene input of Diamond mode mapped fasta results have something wrong.')

    habitat_flag = filecmp.cmp("./tests/diamond_gene/habitat.out.smorfs.tsv", "./examples_output/habitat.out.smorfs.tsv")
    if not habitat_flag:
        print('Gene input of Diamond mode habitat results have something wrong.')

    taxonomy_flag = filecmp.cmp("./tests/diamond_gene/taxonomy.out.smorfs.tsv", "./examples_output/taxonomy.out.smorfs.tsv")
    if not taxonomy_flag:
        print('Gene input of Diamond mode taxonomy results have something wrong.')

    quality_flag = filecmp.cmp("./tests/diamond_gene/quality.out.smorfs.tsv", "./examples_output/quality.out.smorfs.tsv")
    if not quality_flag:
        print('Gene input of Diamond mode quality results have something wrong.')

    summary_flag = filecmp.cmp("./tests/diamond_gene/summary.txt", "./examples_output/summary.txt")
    if not summary_flag:
        print('Gene input of Diamond mode summary results have something wrong.')

    if alignment_flag and fasta_flag and habitat_flag and taxonomy_flag and quality_flag and summary_flag:
        print('Gene input of Diamond mode checking has passed')

    return(alignment_flag,fasta_flag,habitat_flag,taxonomy_flag,quality_flag,summary_flag)

diamond_gene_test()