import pandas as pd

from os import path


def judgefunc(x):
    x = x.split(',')
    if 'high quality' in x:
        return 'high quality'
    else:
        return 'low quality'
    

def smorf_quality(outdir:str, qualityfile:str, resultfile:str) -> tuple:
    result = pd.read_csv(resultfile,
                         sep='\t',
                         header=None)
    
    result = result.rename({0:'qseqid', 1:'sseqid'},
                           axis=1)
    
    quality_file = path.join(outdir,
                             "quality.out.smorfs.tsv")	
    
    ref_quality =  pd.read_table(qualityfile,
                                 sep="\t",
                                 header=None)

    ref_quality.columns = ['sseqid']
    ref_quality['quality'] = 'high quality'

    output = result.merge(on='sseqid',
                          right=ref_quality,
                          how='left')
    
    output = output[['qseqid', 'quality']]
    output = output.fillna('low quality')
    
    output = output.groupby('qseqid',
                            as_index=False,
                            sort=False)
    
    output = output.agg({'quality': lambda x: ','.join(x.drop_duplicates())})  
    output['quality'] = output['quality'].apply(lambda x: judgefunc(x))
    output = output.sort_values(by='qseqid')
    
    number_dict = dict(output['quality'].value_counts())
    number_dict_normalize = dict(output['quality'].value_counts(normalize=True))
    
    if "high quality" in number_dict.keys():
        number = number_dict['high quality']
        percentage = number_dict_normalize['high quality']
    else:
        number = 0
        percentage = 0
    
    output.to_csv(quality_file,
                  sep='\t',
                  index=False)
    
    return (number, percentage)
