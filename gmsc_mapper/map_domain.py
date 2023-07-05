import pandas as pd
from os import path

def fixdf(x):
    x = x.dropna()
    x = x.drop_duplicates()
    return ','.join(x)

def formatlabel(x):
    x = x.split(',')
    x = list(set(x))
    x = sorted(x)
    return ','.join(x)

def store_domain(cddfile): 
    cdd = pd.read_table(cddfile, sep='\t', header=None, names=['gmsc','cdd'])
    cdd_dict = dict(zip(cdd['gmsc'],cdd['cdd']))
    return cdd_dict

def smorf_domain(cddfile, outdir, resultfile):
    cdd_file = path.join(outdir, "domain.out.smorfs.tsv")

    result = pd.read_csv(resultfile,
                         sep='\t',
                         header=None)                       
    result.rename({0: 'qseqid', 1: 'sseqid'},
                  axis=1,
                  inplace=True)
    mapped_sseqid = result['sseqid'].to_list()

    cdd_dict = store_domain(cddfile)

    mapped_sseqid_cdd = {}
    for item in mapped_sseqid:
        if item in cdd_dict.keys():
            mapped_sseqid_cdd[item] = cdd_dict[item]
    result['cdd'] = result['sseqid'].map(lambda g: mapped_sseqid_cdd.get(g))

    output = result[['qseqid', 'cdd']]
    output = output.sort_values(by='qseqid')
    output = output.groupby('qseqid',
                            as_index=False,
                            sort=False) 
    output = output.agg({'cdd':lambda x : fixdf(x)})
    output['cdd'] = output['cdd'].apply(lambda x: formatlabel(x))
    output.to_csv(cdd_file,
                  sep='\t',
                  index=False)    
    
    annotated = output[output['cdd']!='']['cdd'].count()
    return annotated