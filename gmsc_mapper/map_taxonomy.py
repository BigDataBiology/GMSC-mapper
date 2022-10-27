import numpy as np
import pandas as pd

from os import path

def smorf_taxonomy(taxfile:str, resultfile:str ,tmpdirname: str) -> str:
    print('Start taxonomy mapping...')       
    result =  pd.read_csv(resultfile,
                          sep="\t",
                          header=None)
    
    result = result.rename({0:'qseqid',
                            1:'sseqid'},
                           axis=1)

    taxonomy_file = path.join(tmpdirname,
                              "taxonomy.out.smorfs.tmp.tsv") 
    
    reader =  pd.read_table(taxfile,
                            sep="\t",
                            chunksize=5_000_000,
                            header=None,
                            names=['sseqid', 'taxonomy'])

    output_list = []
    for chunk in reader:
        output_chunk = result.merge(on='sseqid',
                                    right=chunk,
                                    how='inner')
        output_chunk = output_chunk[['qseqid',
                                     'sseqid',
                                     'taxonomy']]
        output_list.append(output_chunk)
    
    output = pd.concat(output_list,
                       axis=0)
    
    output = output.sort_values(by='qseqid')
    
    output.to_csv(taxonomy_file,
                  sep='\t',
                  index=False,
                  header=False)
    
    print('Finish taxonomy mapping.')
    return taxonomy_file
    

def fixformat(x):
    x = x.split(';')
    while len(x) < 7:
        x.append('')
    return ';'.join(x)


def reducetab(df):
    df = df.drop_duplicates()
    cols = list(df.columns)
    tax, keepflag = [dict(), 0]
    for i in cols:
        if keepflag:
            tax[i] = ''
        else:
            w = df.loc[df[i] != '', i]
            w = w.value_counts()
            if len(w) != 1:
                tax[i] = ''
                keepflag = 1
            else:
                w = w.index[0]
                tax[i] = w
    tax_flag = [tax.get(t, '') for t in 'dpcofgs']
    tax_flag = ';'.join(tax_flag)
    while ';;' in tax_flag:
         tax_flag = tax_flag.replace(';;', ';')     
    if tax_flag.endswith(';'):
        tax_flag = tax_flag[:-1]
    return tax_flag


def deep_lca(taxfile, outdirname, resultfile, tmpdirname):
    taxonomy_file = smorf_taxonomy(taxfile,
                                   resultfile,
                                   tmpdirname)
    
    taxonomy_dlca_file = path.join(outdirname,
                                   "taxonomy.out.smorfs.tsv")
                                   
    data = pd.read_table(taxonomy_file,
                         header=None,
                         names=['smorf', 'gmsc', 'taxonomy'])

    data = data.fillna('')
    data.taxonomy = data.taxonomy.apply(lambda x: fixformat(x))
    data = data.groupby('smorf').apply(lambda x: x.taxonomy.tolist())
    data = data.reset_index()
    data = data.rename({0: 'taxonomy'}, axis=1)
    
    lca_list = []
    for _, smorf, tax in data.itertuples():
        tax = [x.split(';') for x in tax]
        tax = pd.DataFrame(tax,
                           columns=list('dpcofgs'))
        tax = reducetab(tax)
        lca_list.append((smorf, tax))                                    
    
    lca_list = pd.DataFrame(lca_list,
                            columns=['q_seqid',
                                     'taxonomy'])
    
    lca_list.to_csv(taxonomy_dlca_file,
                    sep='\t', 
                    header=True, 
                    index=None)
   
   
def taxa_summary(outdir):
    taxonomy_dlca_file = path.join(outdir,"taxonomy.out.smorfs.tsv")

    output = pd.read_csv(taxonomy_dlca_file, sep='\t')

    rank = {1:'kingdom',
            2:'phylum',
            3:'class',
            4:'order',
            5:'family',
            6:'genus',
            7:'species',
            8:'no rank'}

    wdf = output['taxonomy'].fillna(';;;;;;;')        

    number_dict = dict(wdf.apply(lambda x: len(x.split(';'))).value_counts())
    number_dict_percentage = dict(wdf.apply(lambda x: len(x.split(';'))).value_counts(normalize=True))

    rank_number = {}
    rank_percentage = {}
    for i in range(1,9):
        if i in number_dict.keys():
            rank_number[rank[i]] = number_dict[i]
            rank_percentage[rank[i]] = number_dict_percentage[i]
        else:
            rank_number[rank[i]] = 0
            rank_percentage[rank[i]] = 0

    annotated_number = output['taxonomy'].size - rank_number['no rank']

    return (annotated_number, rank_number, rank_percentage)			
