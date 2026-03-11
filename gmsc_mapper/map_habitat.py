import pandas as pd
import numpy as np
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

def load_index_to_habitat(indexfile):
    index_habitat = pd.read_csv(indexfile,
                                sep='\t',
                                header=None,
                                names=['index','habitat'])
    return index_habitat['habitat'].to_dict()


def smorf_habitat(indexfile, outdir, habitatfile, resultfile):
    habitat_file = path.join(outdir, "habitat.out.smorfs.tsv")	

    result = pd.read_csv(resultfile,
                         sep='\t',
                         header=None,
                         comment='#')
    result.rename({0: 'qseqid', 1: 'sseqid'},
                  axis=1,
                  inplace=True)
    result['sseqid'] = result['sseqid'].apply(lambda x: int(x.split('.')[2].replace('_','')))
    mapped_sseqid = result['sseqid'].to_list()

    index_habitat_dict = load_index_to_habitat(indexfile)

    habitat = np.load(habitatfile,mmap_mode='r')

    mapped_sseqid_habitat = {}
    for item in mapped_sseqid:
        mapped_sseqid_habitat[item] = index_habitat_dict[habitat[item]]
    result['habitat'] = result['sseqid'].map(lambda g: mapped_sseqid_habitat.get(g))

    output = result[['qseqid', 'habitat']]
    output = output.sort_values(by='qseqid')
    output = output.groupby('qseqid',
                            as_index=False,
                            sort=False) 
    output = output.agg({'habitat':lambda x : fixdf(x)})
    output['habitat'] = output['habitat'].apply(lambda x: formatlabel(x))
    with open_output(habitat_file) as out:
        write_version_comment(out)
        output.to_csv(out,
                      sep='\t',
                      index=False)

    wdf = output['habitat'].apply(lambda x: len(x.split(',')))
    number_dict = dict(wdf.value_counts())
    number_dict_normalize = dict(wdf.value_counts(normalize=True))

    if 1 in number_dict.keys():
        single_number = number_dict[1]
        single_percentage = number_dict_normalize[1]
    else:
        single_number = 0
        single_percentage = 0
        
    multi_number = output['habitat'].size - single_number
    multi_percentage = 1 - single_percentage
    
    return (single_number, single_percentage, multi_number, multi_percentage)
