import pandas as pd
from os import path

def smorf_habitat(outdir,habitatfile,resultfile):
    habitat_file = path.join(outdir,"habitat.out.smorfs.tsv")	

    result = pd.read_csv(resultfile, sep='\t',header=None)
    result = result.rename(columns={0:'qseqid',1:'sseqid'})
    ref_habitat = pd.read_csv(habitatfile, sep='\t',header=None)
    ref_habitat.columns = ['sseqid','habitat']

    output = pd.merge(result,ref_habitat,how='left')[['qseqid', 'habitat']]
    output = output.groupby('qseqid',as_index=False,sort=False).agg({'habitat':lambda x : ','.join(x.dropna().drop_duplicates())})
    output['habitat'] = output['habitat'].apply(lambda x: ','.join(sorted(list(set(x.split(','))))))

    number_dict = dict(output['habitat'].apply(lambda x: len(x.split(','))).value_counts())
    number_dict_normalize = dict(output['habitat'].apply(lambda x: len(x.split(','))).value_counts(normalize=True))
    single_number = number_dict[1]
    single_percentage = number_dict_normalize[1]
    multi_number = output['habitat'].size - single_number
    multi_percentage = 1 - number_dict_normalize[1]

    output.to_csv(habitat_file,sep='\t',index=False)
    return single_number,single_percentage,multi_number,multi_percentage