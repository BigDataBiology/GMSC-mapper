import pandas as pd
from os import path

def smorf_habitat(outdir,habitatfile,resultfile):
    habitat_file = path.join(outdir,"habitat.out.smorfs.tsv")	

    result = pd.read_csv(resultfile,sep='\t',header=None)
    result = result.rename(columns={0:'qseqid',1:'sseqid'})
    if habitatfile.endswith('.gz'):
        reader =  pd.read_csv(habitatfile,compression="gzip",sep="\t",chunksize=5000000,header=None)
    if habitatfile.endswith('.xz'):
        reader =  pd.read_csv(habitatfile,compression="xz",sep="\t",chunksize=5000000,header=None)
    if habitatfile.endswith('.bz2'):
        reader =  pd.read_csv(habitatfile,compression="bz2",sep="\t",chunksize=5000000,header=None)
    else:
        reader =  pd.read_csv(habitatfile,sep="\t",chunksize=5000000,header=None)

    output_list = []
    for chunk in reader:
        chunk.columns = ['sseqid','habitat']
        output_chunk = pd.merge(result,chunk,how='left')[['qseqid', 'habitat']]
        output_list.append(output_chunk)
    output = pd.concat(output_list, axis=0).sort_values(by='qseqid')
    output = output.groupby('qseqid',as_index=False,sort=False).agg({'habitat':lambda x : ','.join(x.dropna().drop_duplicates())})
    output['habitat'] = output['habitat'].apply(lambda x: ','.join(sorted(list(set(x.split(','))))))
    output.to_csv(habitat_file,sep='\t',index=False)

    number_dict = dict(output['habitat'].apply(lambda x: len(x.split(','))).value_counts())
    number_dict_normalize = dict(output['habitat'].apply(lambda x: len(x.split(','))).value_counts(normalize=True))
    if 1 in number_dict.keys():
        single_number = number_dict[1]
        single_percentage = number_dict_normalize[1]
    else:
        single_number = 0
        single_percentage = 0
    multi_number = output['habitat'].size - single_number
    multi_percentage = 1 - single_percentage
    
    return single_number,single_percentage,multi_number,multi_percentage