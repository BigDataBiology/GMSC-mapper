import pandas as pd
from os import path

from gmsc_mapper.utils import open_output, write_version_comment

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
                         header=None,
                         comment='#')
    result.rename({0: 'qseqid', 1: 'sseqid'},
                  axis=1,
                  inplace=True)
    mapped_sseqid = result['sseqid'].to_list()

    cdd_dict = store_domain(cddfile)

    mapped_sseqid_cdd = {}
    for item in mapped_sseqid:
        if item in cdd_dict:
            mapped_sseqid_cdd[item] = cdd_dict[item]
    result['cdd'] = result['sseqid'].map(mapped_sseqid_cdd.get)

    output = result[['qseqid', 'cdd']]
    output = output.sort_values(by='qseqid')
    output = output.groupby('qseqid',
                            as_index=False,
                            sort=False)
    output = output.agg({'cdd': fixdf})
    output['cdd'] = output['cdd'].apply(formatlabel)
    with open_output(cdd_file) as out:
        write_version_comment(out)
        output.to_csv(out,
                      sep='\t',
                      index=False)
    
    annotated = output[output['cdd']!='']['cdd'].count()
    return annotated
