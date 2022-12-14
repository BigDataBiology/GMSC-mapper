import subprocess
import argparse
import sys
import os
from os import path
import pandas as pd
import tempfile
from atomicwrites import atomic_write
import logging

_ROOT = path.abspath(path.join(os.getcwd(), ".."))

logger = logging.getLogger('GMSC-mapper')

def parse_args(args):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='GMSC-mapper')
    subparsers = parser.add_subparsers(title='GMSC-mapper subcommands',
                                       dest='cmd',
                                       metavar='')

    cmd_create_db = subparsers.add_parser('createdb', 
                                          help='Create target database')
    cmd_create_db.add_argument('-i',
                               required=True,
                               help='Path to the GMSC FASTA file.',
                               dest='target_faa',
                               default = None)
    cmd_create_db.add_argument('-o', '--output',
                               required=False,
                               help='Path to database output directory.',
                               dest='output',
                               default = path.join(_ROOT, 'db'))
    cmd_create_db.add_argument('-m', '--mode',
                               required=True,
                               help='Alignment tool (Diamond / MMseqs2)',
                               dest='mode',
                               default = None)
    cmd_create_db.add_argument('--quiet',
                                action='store_true',
                                dest='quiet',
                                help='Disable alignment console output')

    parser.add_argument('-i', '--input',
                        required=False,
                        help='Path to the input genome contig sequence FASTA file.',
                        dest='genome_fasta',
                        default = None)

    parser.add_argument('--nt-genes', '--nt_genes',
                        required=False,
                        help='Path to the input nucleotide gene sequence FASTA file.',
                        dest='nt_input',
                        default=None)

    parser.add_argument('--aa-genes', '--aa_genes',
                        required=False,
                        help='Path to the input amino acid sequence FASTA file.',
                        dest='aa_input',
                        default=None)

    parser.add_argument('-o', '--output',
                        required=False,
                        help='Output directory (will be created if non-existent)',
                        dest='output',
                        default=path.join(_ROOT, 'output'))
 
    parser.add_argument('--tool', '--tool',
                        required=False,
                        choices=['diamond', 'mmseqs'],
                        help='Sequence alignment tool (Diamond / MMseqs).',
                        dest='tool',
                        default='diamond')

    parser.add_argument('-s', '--sensitivity',
                        required=False,
                        help='Sensitivity.',
                        dest='sensitivity')

    parser.add_argument('--id', '--id',
                        required=False,
                        help='Minimum identity to report an alignment (range 0.0-1.0).',
                        dest='identity',
                        default=0.0)

    parser.add_argument('--cov', '--cov',
                        required=False,
                        help='Minimum coverage to report an alignment (range 0.0-1.0).',
                        dest='coverage',
                        default=0.9)

    parser.add_argument('-e', '--evalue',
                        required=False,
                        help='Maximum e-value to report alignments.',
                        dest='evalue',
                        default=0.00001)

    parser.add_argument('-t', '--threads',
                        required=False,
                        help='Number of CPU threads.',
                        dest='threads',
                        default=1)

    parser.add_argument('--filter','--filter',action='store_true', help='Use this to filter <100 aa or <303 nt input sequences.')

    parser.add_argument('--nohabitat','--nohabitat',action='store_true', help='Use this if no need to annotate habitat')

    parser.add_argument('--notaxonomy', '--notaxonomy',action='store_true', help='Use this if no need to annotate taxonomy')

    parser.add_argument('--noquality', '--noquality',action='store_true', help='Use this if no need to annotate quality')
    
    parser.add_argument('--quiet','--quiet',action='store_true', help='Disable alignment console output')

    parser.add_argument('--db', '--db',
                        required=False,
                        help='Path to the GMSC database file.',
                        dest='database')

    parser.add_argument('--habitat', '--habitat',
                        required=False,
                        help='Path to the habitat file',
                        dest='habitat',
                        default=path.join(_ROOT, 'db/ref_habitat.npy'))

    parser.add_argument('--habitat-index', '--habitat-index',
                        required=False,
                        help='Path to the habitat index file',
                        dest='habitatindex',
                        default=path.join(_ROOT, 'db/ref_habitat_index.tsv'))

    parser.add_argument('--taxonomy', '--taxonomy',
                        required=False,
                        help='Path to the taxonomy file',
                        dest='taxonomy',
                        default=path.join(_ROOT, 'db/ref_taxonomy.npy'))

    parser.add_argument('--taxonomy-index', '--taxonomy-index',
                        required=False,
                        help='Path to the taxonomy index file',
                        dest='taxonomyindex',
                        default=path.join(_ROOT, 'db/ref_taxonomy_index.tsv'))

    parser.add_argument('--quality', '--quality',
                        required=False,
                        help='Path to the quality file',
                        dest='quality',
                        default=path.join(_ROOT, 'db/ref_quality.tsv.xz'))

    return parser.parse_args()

def check_install():
    from shutil import which
    import sys
    
    has_mmseqs = False
    has_diamond = False
    dependencies = ['diamond', 'mmseqs']
    logger.debug("Looking for dependencies...")

    for dep in dependencies:
        p = which(dep)
        if p:
            if dep == 'diamond':
                has_diamond = True
            if dep == 'mmseqs':
                has_mmseqs = True
    if not has_diamond and not has_mmseqs:
        sys.stderr.write('GMSC-mapper Error: Neither diamond nor mmseqs appear to be available!\n'
                        'At least one of them is necessary to run GMSC-mapper.\n')
        sys.exit(1)
    elif has_diamond and not has_mmseqs:
        logger.warning('Warning: mmseqs does not appear to be available.You can only use the `--tool diamond` option(default).')
    elif not has_diamond and has_mmseqs:
        logger.warning('Warning: diamond does not appear to be available.You can only use the `--tool mmseqs` option.')
    else:
        logger.info('Dependencies installation is OK\n')
    return has_diamond,has_mmseqs

def validate_args(args,has_diamond,has_mmseqs):
    def expect_file(f):
        if not os.path.exists(f):
            sys.stderr.write(f"GMSC-mapper Error: Expected file '{f}' does not exist\n")
            sys.exit(1)
    
    if not args.genome_fasta and not args.aa_input and not args.nt_input:
        pass
    elif args.genome_fasta and not args.aa_input and not args.nt_input:
        expect_file(args.genome_fasta)
    elif args.aa_input and not args.genome_fasta and not args.nt_input:
        expect_file(args.aa_input)
    elif args.nt_input and not args.genome_fasta and not args.aa_input:
        expect_file(args.nt_input)
    else:
        sys.stderr.write("GMSC-mapper Error: --input or --aa-genes or --nt_genes shouldn't be assigned at the same time\n")
        sys.exit(1)
    
    if args.tool == "diamond" and not has_diamond:
        sys.stderr.write("GMSC-mapper Error:diamond is not available.Please add diamond into your path or use the `--tool mmseqs` option.\n")
        sys.exit(1)       
    if args.tool == "mmseqs" and not has_mmseqs:
        sys.stderr.write("GMSC-mapper Error:mmseqs is not available.Please add mmseqs into your path or use the `--tool diamond` option(default).\n")
        sys.exit(1)

    if args.database:
        expect_file(args.database)      

    if not args.nohabitat and args.habitat:
        expect_file(args.habitat)

    if not args.notaxonomy and args.taxonomy:
        expect_file(args.taxonomy)

    if not args.noquality and args.quality:
        expect_file(args.quality)

def create_db(args):
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    out_db = path.join(args.output,"targetdb")

    if args.quiet:
        diamond_cmd = ['diamond','makedb',
                        '--in',args.target_faa,
                        '-d',out_db,
                        '--quiet']
        mmseqs_cmd = ['mmseqs','createdb',
                        args.target_faa,
                        out_db,
                        '-v','0']    
    else:                    
        diamond_cmd = ['diamond','makedb',
                    '--in',args.target_faa,
                    '-d',out_db]
        mmseqs_cmd = ['mmseqs','createdb',
                    args.target_faa,
                    out_db]

    if args.mode == "diamond":
        logger.info('Start creating Diamond database...')
        subprocess.check_call(diamond_cmd)
        logger.info('Diamond database has been created successfully.')

    if args.mode == "mmseqs":
        logger.debug('Start creating MMseqs database...')
        subprocess.check_call(mmseqs_cmd)
        logger.info('MMseqs database has been created successfully.')

def predict(args,tmpdir):
    from gmsc_mapper.predict import predict_genes,filter_smorfs

    logger.debug('Starting smORF prediction...')

    predicted_smorf = path.join(tmpdir,"predicted.smorf.faa")
    filtered_smorf = path.join(args.output,"predicted.filterd.smorf.faa")

    predict_genes(args.genome_fasta,predicted_smorf)
    if not path.getsize(predicted_smorf):
        sys.stderr.write("GMSC-mapper Error:No smORFs have been predicted.Please check your input file.\n")
        sys.exit(1)
    else:
        filter_smorfs(predicted_smorf, filtered_smorf)
    if not path.getsize(filtered_smorf):
        sys.stderr.write("GMSC-mapper Error:No smORFs remained after filtering by length(<100aa).\n")
        sys.exit(1)
    else:
        logger.info('smORF prediction complete')
    return filtered_smorf

def translate_gene(args,tmpdir):
    from gmsc_mapper.translate import translate_gene
    logger.debug('Starting gene translation...')
    translated_file = translate_gene(args.nt_input,tmpdir)
    logger.info('Gene translation complete')
    return translated_file

def check_length(queryfile):
    from gmsc_mapper.fasta import fasta_iter
    logger.debug('Start length checking...')
    if all(len(seq) < 303
                for _, seq in fasta_iter(queryfile)):
        logger.warning('GMSC-mapper Warning: Input sequences are all more than 303nt. '
                       'Please check if your input consists of contigs, which should use -i not --nt-genes or --aa-genes as input. '
                       'However, we will regard your input sequences as nucleotide genes and continue to process.\n')

    logger.info('Length checking has done.\n')

def filter_length(queryfile,tmpdir,N):
    from gmsc_mapper.filter_length import filter_length
    logger.debug('Starting length filter...')
    filtered_file = filter_length(queryfile,tmpdir,N)
    logger.info('Length filter complete')
    return filtered_file

def mapdb_diamond(args,queryfile):
    logger.debug('Starting smORF mapping...')

    resultfile = path.join(args.output,"alignment.out.smorfs.tsv")
    outfmt = '6,qseqid,sseqid,full_qseq,full_sseq,qlen,slen,length,qstart,qend,sstart,send,bitscore,pident,evalue,qcovhsp,scovhsp'

    diamond_cmd = ['diamond','blastp',
                    '-q',queryfile,
                    '-d',args.database,
                    '-o',resultfile,
                    args.sensitivity,
                    '-e',str(args.evalue),
                    '--id',str(float(args.identity)*100),
                    '--query-cover',str(float(args.coverage)*100),
                    '--subject-cover',str(float(args.coverage)*100),
                    '-p',str(args.threads),
                    '--outfmt'] + outfmt.split(',')
    if args.quiet:
        diamond_cmd.append('--quiet')

    subprocess.check_call(diamond_cmd)

    logger.info('smORF mapping complete')
    return resultfile

def mapdb_mmseqs(args, queryfile, tmpdir):
    logger.info('Start smORF mapping...')

    querydb = path.join(tmpdir,"query.db")
    resultdb = path.join(tmpdir,"result.db")
    tmp = path.join(tmpdir,"tmp","")
    resultfile = path.join(args.output,"alignment.out.smorfs.tsv")
    outfmt = 'query,target,qseq,tseq,qlen,tlen,alnlen,qstart,qend,tstart,tend,bits,pident,evalue,qcov,tcov'

    mmseqs_cmd_db = ['mmseqs', 'createdb', queryfile, querydb]
    mmseqs_cmd_search = ['mmseqs','search',
                        querydb,
                        args.database,
                        resultdb,
                        tmp,
                        '-s',str(args.sensitivity),
                        '-e',str(args.evalue),
                        '--min-seq-id',str(args.identity),
                        '-c',str(args.coverage),
                        '--threads',str(args.threads)]
    mmseqs_cmd_out = ['mmseqs','convertalis',
                    querydb,
                    args.database,
                    resultdb,
                    resultfile,
                    '--format-output', outfmt]
    for mmseqs_cmd in [mmseqs_cmd_db,mmseqs_cmd_search,mmseqs_cmd_out]:
        if args.quiet:
            mmseqs_cmd.extend(['-v', '0'])
        subprocess.check_call(mmseqs_cmd)

    logger.info('smORF mapping complete')
    return resultfile

def generate_fasta(output,queryfile,resultfile):
    import pandas as pd
    from gmsc_mapper.fasta import fasta_iter

    try:
        result = pd.read_csv(resultfile, sep='\t',header=None)
    except:
        logger.error('GMSC-mapper error: There is no alignment results between your input sequences and GMSC.\n')
        sys.exit(1)

    logger.debug('Start smORF fasta file generation...')
    fastafile = path.join(output,"mapped.smorfs.faa")

    smorf_id = set(result.iloc[:, 0].tolist())
    
    with open(fastafile,"wt") as f:
        for ID,seq in fasta_iter(queryfile):
            if ID in smorf_id:
                f.write(f'>{ID}\n{seq}\n')
    logger.debug('smORF fasta file generation complete')
    return fastafile

def habitat(args,resultfile):
    from gmsc_mapper.map_habitat import smorf_habitat
    logger.debug('Starting habitat annotation...')
    single_number,single_percentage,multi_number,multi_percentage = smorf_habitat(args.habitatindex,args.output,args.habitat,resultfile)
    logger.info('habitat annotation has done.')
    return single_number,single_percentage,multi_number,multi_percentage 

def taxonomy(args,resultfile,tmpdirname):
    from gmsc_mapper.map_taxonomy import deep_lca,taxa_summary
    logger.debug('Start taxonomy annotation...')
    deep_lca(args.taxonomyindex,args.taxonomy,args.output,resultfile,tmpdirname)
    annotated_number,rank_number,rank_percentage = taxa_summary(args.output)
    logger.info('Taxonomy annotation complete.')
    return annotated_number,rank_number,rank_percentage

def quality(args,resultfile):
    from gmsc_mapper.map_quality import smorf_quality
    logger.debug('Start quality annotation...')
    number,percentage = smorf_quality(args.output,args.quality,resultfile)
    logger.info('Quality annotation completed.')
    return number,percentage

def predicted_smorf_count(file_name):
    return sum(1 for _ in open(file_name, 'rt'))

def main(args=None):
    if args is None:
        args = sys.argv
    args = parse_args(args)
    if not args.cmd and (not args.genome_fasta and not args.aa_input and not args.nt_input):
        sys.stderr.write("GMSC-mapper Error: Please see gmsc-mapper -h. Assign the subcommand or input file.\n")
        sys.exit(1)             
    has_diamond,has_mmseqs = check_install()

    if args.cmd == 'createdb':
        create_db(args)

    if not args.cmd:
        validate_args(args,has_diamond,has_mmseqs)

        if args.tool == 'diamond':
            if args.database is None:
                args.database = path.join(_ROOT, 'db/targetdb.dmnd')
            args.sensitivity = {
                None: '--more-sensitive',
                '1': '--fast',
                '2': '--mid-sensitive',
                '3': '--default',
                '4': '--sensitive',
                '5': '--more-sensitive',
                '6': '--very-sensitive',
                '7': '--ultra-sensitive',
            }.get(args.sensitivity, args.sensitivity)

        if args.tool == 'mmseqs':
            if args.database is None:
                args.database = path.join(_ROOT, 'db/targetdb')
            if args.sensitivity is None:
                args.sensitivity = 5.7

        os.makedirs(args.output, exist_ok=True)

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                summary = []
                summary.append(f'# Total number')
                if args.genome_fasta:
                    queryfile = predict(args,tmpdir)
                    smorf_number = int(predicted_smorf_count(queryfile)/2)
                    summary.append(f'{smorf_number} smORFs are predicted in total.')
                if args.nt_input:
                    if args.filter:
                        args.nt_input = filter_length(args.nt_input,tmpdir,303)
                    else:
                        check_length(args.nt_input)
                    queryfile = translate_gene(args,tmpdir)  
                if args.aa_input:
                    if args.filter:
                        args.aa_input = filter_length(args.aa_input,tmpdir,100)
                    queryfile = args.aa_input

                if args.tool == 'diamond':
                    resultfile = mapdb_diamond(args,queryfile)
                if args.tool == 'mmseqs':
                    resultfile = mapdb_mmseqs(args,queryfile,tmpdir)

                fastafile = generate_fasta(args.output,queryfile,resultfile)
                smorf_number = int(predicted_smorf_count(fastafile)/2)
                summary.append(f'{smorf_number} smORFs aligned against GMSC in total.\n')

                if not args.noquality:
                    summary.append(f'# Quality')
                    number,percentage = quality(args,resultfile)
                    summary.append(f'{number} ({percentage:.2%}) aligned smORFs are high quality.\n')

                if not args.nohabitat:
                    summary.append(f'# Habitat')
                    single_number,single_percentage,multi_number,multi_percentage = habitat(args,resultfile)
                    summary.append(f'{single_number} ({single_percentage:.2%}) aligned smORFs are single-habitat.')
                    summary.append(f'{multi_number} ({multi_percentage:.2%}) aligned smORFs are multi-habitat.\n')

                if not args.notaxonomy:
                    summary.append(f'# Taxonomy')
                    annotated_number,rank_number,rank_percentage = taxonomy(args,resultfile,tmpdir)	
                    summary.append(str(annotated_number)+'('+str(round((1-rank_percentage['no rank'])*100,2))+'%) aligned smORFs have taxonomy annotation.')
                    summary.append(str(rank_number['kingdom'])+'('+str(round(rank_percentage['kingdom']*100,2))+'%) aligned smORFs are annotated on kingdom.')
                    summary.append(str(rank_number['phylum'])+'('+str(round(rank_percentage['phylum']*100,2))+'%) aligned smORFs are annotated on phylum.')
                    summary.append(str(rank_number['class'])+'('+str(round(rank_percentage['class']*100,2))+'%) aligned smORFs are annotated on class.')
                    summary.append(str(rank_number['order'])+'('+str(round(rank_percentage['order']*100,2))+'%) aligned smORFs are annotated on order.')
                    summary.append(str(rank_number['family'])+'('+str(round(rank_percentage['family']*100,2))+'%) aligned smORFs are annotated on family.')
                    summary.append(str(rank_number['genus'])+'('+str(round(rank_percentage['genus']*100,2))+'%) aligned smORFs are annotated on genus.')
                    summary.append(str(rank_number['species'])+'('+str(round(rank_percentage['species']*100,2))+'%) aligned smORFs are annotated on species.')

                with atomic_write(f'{args.output}/summary.txt', overwrite=True) as ofile:
                    for s in summary:
                        print(s)
                        ofile.write(f'{s}\n')		

            except Exception as e:
                sys.stderr.write('GMGC-mapper Error: ')
                sys.stderr.write(str(e))
                sys.stderr.write('\n')
                sys.exit(1)		

if __name__ == '__main__':    
    main(sys.argv)
