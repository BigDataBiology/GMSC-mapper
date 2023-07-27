import subprocess
import argparse
import sys
import os
from os import path
import pandas as pd
import tempfile
from atomicwrites import atomic_write
import logging

_ROOT = path.abspath(path.join(os.getcwd(), "."))

logger = logging.getLogger('GMSC-mapper')

def parse_args(args):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='GMSC-mapper')
    subparsers = parser.add_subparsers(title='GMSC-mapper subcommands',
                                       dest='cmd',
                                       metavar='')
    
    cmd_download_db = subparsers.add_parser('downloaddb', 
                                          help='Download target database')
    
    cmd_download_db.add_argument('--dbdir',
                               required=False,
                               help='Path to the database files.',
                               dest='dbdir',
                               default = path.join(_ROOT, 'db'))
    cmd_download_db.add_argument('--all', action="store_true", dest='all',
                                help='Download all database')
    cmd_download_db.add_argument('-f', action="store_true", dest='force',
                                help='Force download even if the files exist')
    
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

    parser.add_argument('--no-habitat','--no-habitat',action='store_true', dest='nohabitat', help='Use this if no need to annotate habitat')

    parser.add_argument('--no-taxonomy', '--no-taxonomy',action='store_true', dest='notaxonomy', help='Use this if no need to annotate taxonomy')

    parser.add_argument('--no-quality', '--no-quality',action='store_true', dest='noquality', help='Use this if no need to annotate quality')
    
    parser.add_argument('--no-domain', '--no-domain',action='store_true', dest='nodomain', help='Use this if no need to annotate quality')

    parser.add_argument('--quiet','--quiet',action='store_true', help='Disable alignment console output')
    
    parser.add_argument('--dbdir', '--dbdir',
                        required=False,
                        help='Path to the GMSC database directory.',
                        dest='dbdir',
                        default = path.join(_ROOT, 'db'))

    return parser.parse_args(args[1:])

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
        logger.warning('GMSC-mapper Warning: Neither diamond nor mmseqs appear to be available! It will download diamond and mmseqs.\n')
        subprocess.check_call(['wget','https://mmseqs.com/latest/mmseqs-linux-avx2.tar.gz',
                                '-P','./bin'])
        subprocess.check_call(['tar','xvfz',
                                './bin/mmseqs-linux-avx2.tar.gz',
                                '-C','./bin'])
        subprocess.check_call(['wget','http://github.com/bbuchfink/diamond/releases/download/v2.1.8/diamond-linux64.tar.gz',
                                '-P','./bin'])
        subprocess.check_call(['tar','xvfz',
                                './bin/diamond-linux64.tar.gz',
                                '-C','./bin'])
    else:
        logger.info('Dependencies installation is OK\n')
    return has_diamond,has_mmseqs

def validate_args(args,has_diamond,has_mmseqs):
    def expect_file(f):
        if not os.path.exists(f):
            sys.stderr.write(f"GMSC-mapper Error: Expected file '{f}' does not exist\n")
            sys.exit(1)

    def expect_database(f):
        if not os.path.exists(f):
            sys.stderr.write(f"GMSC-mapper Error: Expected file '{f}' does not exist. Please use --dbdir to assign your database directory.\n")
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
        logger.warning("GMSC-mapper Warning:mmseqs is not available.It will download diamond.\n")
        subprocess.check_call(['wget','http://github.com/bbuchfink/diamond/releases/download/v2.1.8/diamond-linux64.tar.gz',
                                '-P','./bin'])
        subprocess.check_call(['tar','xvfz',
                                './bin/diamond-linux64.tar.gz',
                                '-C','./bin'])      
    if args.tool == "mmseqs" and not has_mmseqs:
        logger.warning("GMSC-mapper Warning:mmseqs is not available.It will download mmseqs.\n")
        subprocess.check_call(['wget','https://mmseqs.com/latest/mmseqs-linux-avx2.tar.gz',
                                '-P','./bin'])
        subprocess.check_call(['tar','xvfz',
                                './bin/mmseqs-linux-avx2.tar.gz',
                                '-C','./bin'])
    
    if args.tool == "diamond":
        expect_database(path.join(args.dbdir, "diamond_targetdb.dmnd"))
    if args.tool == "mmseqs":
        expect_database(path.join(args.dbdir, "mmseqs_targetdb"))

    if not args.nohabitat:
        expect_database(path.join(args.dbdir, "GMSC10.90AA.habitat.index.tsv"))
        expect_database(path.join(args.dbdir, "GMSC10.90AA.habitat.npy"))

    if not args.notaxonomy:
        expect_database(path.join(args.dbdir, "GMSC10.90AA.taxonomy.index.tsv"))
        expect_database(path.join(args.dbdir, "GMSC10.90AA.taxonomy.npy"))

    if not args.noquality:
        expect_database(path.join(args.dbdir, "GMSC10.90AA.high_quality.tsv.xz"))

    if not args.nodomain:
        expect_database(path.join(args.dbdir, "GMSC10.90AA.cdd.tsv.xz"))

def download_db(args):
    from gmsc_mapper.utils import ask

    if args.force or not os.path.exists(os.path.join(args.dbdir,'GMSC10.90AA.faa.gz')):
        if args.all or ask("Download 90AA fasta file (~11G)?") == 'y':
            logger.info('Start downloading 90AA fasta file...')
            subprocess.check_call(['wget','https://gmsc-api.big-data-biology.org/files/GMSC10.90AA.faa.gz',
                                '-P',args.dbdir])
            logger.info('90AA fasta file has been downloaded successfully.')
        else:
            print('Skip downloading 90AA fasta file.')
    else:
        print('90AA fasta file already exists. Skip downloading 90AA fasta file. Use -f to force download')

    if args.force or not os.path.exists(os.path.join(args.dbdir,'GMSC10.90AA.habitat.npy')) or not os.path.exists(os.path.join(args.dbdir,'GMSC10.90AA.habitat.index.tsv')):
        if args.all or ask("Download habitat index file (~2.3G)?") == 'y':
            logger.info('Start downloading habitat index file...')
            subprocess.check_call(['wget','https://gmsc-api.big-data-biology.org/files/GMSC10.90AA.habitat.npy',
                                '-P',args.dbdir])
            subprocess.check_call(['wget','https://gmsc-api.big-data-biology.org/files/GMSC10.90AA.habitat.index.tsv',
                                '-P',args.dbdir])
            logger.info('Habitat index file has been downloaded successfully.')
        else:
            print('Skip downloading habitat index file.')
    else:
        print('Habitat index file already exists. Skip downloading habitat index file. Use -f to force download')

    if args.force or not os.path.exists(os.path.join(args.dbdir,'GMSC10.90AA.taxonomy.npy')) or not os.path.exists(os.path.join(args.dbdir,'GMSC10.90AA.taxonomy.index.tsv')):
        if args.all or ask("Download taxonomy index file (~2.3G)?") == 'y':
            logger.info('Start downloading taxonomy index file...')
            subprocess.check_call(['wget','https://gmsc-api.big-data-biology.org/files/GMSC10.90AA.taxonomy.npy',
                                '-P',args.dbdir])
            subprocess.check_call(['wget','https://gmsc-api.big-data-biology.org/files/GMSC10.90AA.taxonomy.index.tsv',
                                '-P',args.dbdir])
            logger.info('Taxonomy index file has been downloaded successfully.')
        else:
            print('Skip downloading taxonomy index file.')
    else:
        print('Taxonomy index file already exists. Skip downloading taxonomy index file. Use -f to force download')

    if args.force or not os.path.exists(os.path.join(args.dbdir,'GMSC10.90AA.high_quality.tsv.xz')):        
        if args.all or ask("Download quality index file (2.6M)?") == 'y':
            logger.info('Start downloading quality index file...')
            subprocess.check_call(['wget','https://gmsc-api.big-data-biology.org/files/GMSC10.90AA.high_quality.tsv.xz',
                                '-P',args.dbdir])
            logger.info('Quality index file has been downloaded successfully.')
        else:
            print('Skip downloading quality index file.')
    else:
        print('Quality index file already exists. Skip downloading quality index file. Use -f to force download')
 
    if args.force or not os.path.exists(os.path.join(args.dbdir,'GMSC10.90AA.cdd.tsv.xz')):               
        if args.all or ask("Download conserved domain index file (88M)?") == 'y':
            logger.info('Start downloading conserved domain index file...')
            subprocess.check_call(['wget','https://gmsc-api.big-data-biology.org/files/GMSC10.90AA.cdd.tsv.xz',
                                '-P',args.dbdir])
            logger.info('Conserved domain index file has been downloaded successfully.')
        else:
            print('Skip downloading conserved domain index file.')
    else:
        print('Conserved domain index file already exists. Skip downloading conserved domain index file. Use -f to force download')

def create_db(args):
    from shutil import which

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    diamond_out_db = path.join(args.output,"diamond_targetdb")
    mmseqs_out_db = path.join(args.output,"mmseqs_targetdb")
    
    if which('diamond'):
        diamond = 'diamond'
    else:
        diamond = './bin/diamond'
    
    if which('mmseqs'):
        mmseqs = 'mmseqs'
    else:
        mmseqs = './bin/mmseqs/bin/mmseqs'

    if args.quiet:
        diamond_cmd = [diamond,'makedb',
                        '--in',args.target_faa,
                        '-d',diamond_out_db,
                        '--quiet']
        mmseqs_cmd = [mmseqs,'createdb',
                        args.target_faa,
                        mmseqs_out_db,
                        '-v','0']    
    else:                    
        diamond_cmd = [diamond,'makedb',
                    '--in',args.target_faa,
                    '-d',diamond_out_db]
        mmseqs_cmd = [mmseqs,'createdb',
                    args.target_faa,
                    mmseqs_out_db]

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
        logger.info("GMSC-mapper Info:No smORFs have been predicted.Please check your input file.\n")
        return ("",False)
    else:
        filter_smorfs(predicted_smorf, filtered_smorf)
        if not path.getsize(filtered_smorf):
            logger.info("GMSC-mapper Info:No smORFs remained after filtering by length(<100aa).\n")
            return ("",False)
        else:
            logger.info('smORF prediction complete')
            return (filtered_smorf,True)

def translate_gene(args,tmpdir):
    from gmsc_mapper.translate import translate_gene
    logger.debug('Starting gene translation...')
    translated_file = translate_gene(args.nt_input,tmpdir)
    logger.info('Gene translation complete')
    return translated_file

def check_length(queryfile):
    from gmsc_mapper.fasta import fasta_iter
    logger.debug('Start length check...')
    if all(len(seq) < 303
                for _, seq in fasta_iter(queryfile)):
        logger.warning('GMSC-mapper Warning: Input sequences are all greater than 300bps.\n'
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
    from shutil import which

    logger.debug('Starting smORF mapping...')

    resultfile = path.join(args.output,"alignment.out.smorfs.tsv")
    outfmt = '6,qseqid,sseqid,full_qseq,full_sseq,qlen,slen,length,qstart,qend,sstart,send,bitscore,pident,evalue,qcovhsp,scovhsp'

    if which('diamond'):
        diamond = 'diamond'
    else:
        diamond = './bin/diamond'
    
    database = path.join(args.dbdir, "diamond_targetdb.dmnd")
    
    if args.sensitivity != '--default':
        diamond_cmd = [diamond,'blastp',
                    '-q',queryfile,
                    '-d',database,
                    '-o',resultfile,
                    args.sensitivity,
                    '-e',str(args.evalue),
                    '--id',str(float(args.identity)*100),
                    '--query-cover',str(float(args.coverage)*100),
                    '--subject-cover',str(float(args.coverage)*100),
                    '-p',str(args.threads),
                    '--outfmt'] + outfmt.split(',')
    else:
        diamond_cmd = [diamond,'blastp',
                    '-q',queryfile,
                    '-d',database,
                    '-o',resultfile,
                    '-e',str(args.evalue),
                    '--id',str(float(args.identity)*100),                                                                                   '--query-cover',str(float(args.coverage)*100),
                    '--subject-cover',str(float(args.coverage)*100),                                                                        '-p',str(args.threads),                                                                                                 '--outfmt'] + outfmt.split(',')
    if args.quiet:
        diamond_cmd.append('--quiet')

    subprocess.check_call(diamond_cmd)

    logger.info('smORF mapping complete')
    return resultfile

def mapdb_mmseqs(args, queryfile, tmpdir):
    from shutil import which

    logger.info('Start smORF mapping...')

    querydb = path.join(tmpdir,"query.db")
    resultdb = path.join(tmpdir,"result.db")
    tmp = path.join(tmpdir,"tmp","")
    resultfile = path.join(args.output,"alignment.out.smorfs.tsv")
    outfmt = 'query,target,qseq,tseq,qlen,tlen,alnlen,qstart,qend,tstart,tend,bits,pident,evalue,qcov,tcov'

    if which('mmseqs'):
        mmseqs = 'mmseqs'
    else:
        mmseqs = './bin/mmseqs/bin/mmseqs'

    database = path.join(args.dbdir, "mmseqs_targetdb")

    mmseqs_cmd_db = [mmseqs, 'createdb', queryfile, querydb]
    mmseqs_cmd_search = [mmseqs,'search',
                        querydb,
                        database,
                        resultdb,
                        tmp,
                        '-s',str(args.sensitivity),
                        '-e',str(args.evalue),
                        '--min-seq-id',str(args.identity),
                        '-c',str(args.coverage),
                        '--threads',str(args.threads)]
    mmseqs_cmd_out = [mmseqs,'convertalis',
                    querydb,
                    database,
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
        print('GMSC-mapper info: There is no alignment results between your input sequences and GMSC.\n')
        logger.info('GMSC-mapper info: There is no alignment results between your input sequences and GMSC.\n')
        return ("",False)
    else:
        logger.debug('Start smORF fasta file generation...')
        fastafile = path.join(output,"mapped.smorfs.faa")

        smorf_id = set(result.iloc[:, 0].tolist())
    
        with open(fastafile,"wt") as f:
            for ID,seq in fasta_iter(queryfile):
                if ID in smorf_id:
                    f.write(f'>{ID}\n{seq}\n')
        logger.debug('smORF fasta file generation complete')
        return (fastafile,True)

def habitat(args,resultfile):
    from gmsc_mapper.map_habitat import smorf_habitat
    logger.debug('Starting habitat annotation...')

    habitatindex = path.join(args.dbdir, "GMSC10.90AA.habitat.index.tsv")
    habitat = path.join(args.dbdir, "GMSC10.90AA.habitat.npy")
    r_habitat = smorf_habitat(habitatindex,args.output,habitat,resultfile)

    logger.info('habitat annotation has done.')
    return r_habitat

def taxonomy(args,resultfile,tmpdirname):
    from gmsc_mapper.map_taxonomy import deep_lca,taxa_summary
    logger.debug('Start taxonomy annotation...')
    
    taxonomyindex = path.join(args.dbdir, "GMSC10.90AA.taxonomy.index.tsv")
    taxonomy = path.join(args.dbdir, "GMSC10.90AA.taxonomy.npy")
    deep_lca(taxonomyindex,taxonomy,args.output,resultfile,tmpdirname)
    r_summary = taxa_summary(args.output)

    logger.info('Taxonomy annotation complete.')
    return r_summary

def quality(args,resultfile):
    from gmsc_mapper.map_quality import smorf_quality
    logger.debug('Start quality annotation...')

    quality = path.join(args.dbdir, "GMSC10.90AA.high_quality.tsv.xz")
    number,percentage = smorf_quality(args.output,quality,resultfile)

    logger.info('Quality annotation completed.')
    return number,percentage

def domain(args,resultfile):
    from gmsc_mapper.map_domain import smorf_domain
    logger.debug('Start domain annotation...')

    domain = path.join(args.dbdir, "GMSC10.90AA.cdd.tsv.xz")
    number = smorf_domain(domain,args.output,resultfile)
    logger.info('Domain annotation completed.')
    return number

def predicted_smorf_count(file_name):
    return sum(1 for _ in open(file_name, 'rt'))

def main(args=None):
    if args is None:
        args = sys.argv
    args = parse_args(args)
    if not args.cmd and not args.genome_fasta and not args.aa_input and not args.nt_input:
        sys.stderr.write("GMSC-mapper Error: Please see gmsc-mapper -h. Choose a subcommand or input file.\n")
        sys.exit(1)
    has_diamond,has_mmseqs = check_install()

    if args.cmd == 'createdb':
        create_db(args)
    
    if args.cmd == 'downloaddb':
        download_db(args)

    if not args.cmd:
        validate_args(args,has_diamond,has_mmseqs)
        
        if args.tool == 'diamond':
            args.sensitivity = {
                None: '--more-sensitive',
                '1': '--fast',
                '2': '--default',
                '3': '--mid-sensitive',
                '4': '--sensitive',
                '5': '--more-sensitive',
                '6': '--very-sensitive',
                '7': '--ultra-sensitive',
            }.get(args.sensitivity, args.sensitivity)

        if args.tool == 'mmseqs':
            if args.sensitivity is None:
                args.sensitivity = 5.7

        os.makedirs(args.output, exist_ok=True)

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                summary = []
                summary.append(f'# Total number')
                if args.genome_fasta:
                    (queryfile,ifpredict) = predict(args,tmpdir)
                    if ifpredict:
                        smorf_number = int(predicted_smorf_count(queryfile)/2)
                        summary.append(f'{smorf_number} smORFs are predicted in total.')
                    else:
                        summary.append(f'No smORFs are predicted.')
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
                
                if (args.genome_fasta and ifpredict) or args.nt_input or args.aa_input:
                    if args.tool == 'diamond':
                        resultfile = mapdb_diamond(args,queryfile)
                    if args.tool == 'mmseqs':
                        resultfile = mapdb_mmseqs(args,queryfile,tmpdir)

                    (fastafile,ifsuccess) = generate_fasta(args.output,queryfile,resultfile)
                    if ifsuccess:
                        smorf_number = int(predicted_smorf_count(fastafile)/2)
                        summary.append(f'{smorf_number} smORFs are aligned against GMSC in total.\n')

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
                            summary.append(f'{annotated_number} ({1 - rank_percentage["no rank"]:.2%}) aligned smORFs have taxonomy annotation.')
                            for rank in ['kingdom','phylum','class','order','family','genus','species']:
                                summary.append(f'{rank_number[rank]} ({rank_percentage[rank]:.2%}) aligned smORFs are annotated at level of {rank}.')

                        if not args.nodomain:
                            summary.append(f'\n# Conserved domain')
                            number = domain(args,resultfile)
                            summary.append(f'{number} aligned smORFs are annotated with CDD database.\n')
                    else:
                        summary.append(f'None of sequences are aligned against GMSC.\n')
                
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
