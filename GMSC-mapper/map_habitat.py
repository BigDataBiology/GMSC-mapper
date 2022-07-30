# how to solve memory/time consuming
# adapt to different format(.xz .gz)
import pandas as pd
from os import path

def smorf_habitat(args,resultfile):
    habitat_file = path.join(args.output,"habitat.out.smorfs.tsv")	

    result = pd.read_csv(resultfile, sep='\t',header=None)
    result.columns = ['qseqid','full_qseq','qlen','sseqid','full_sseq','slen','pident','length','evalue','qcovhsp','scovhsp']
    ref_habitat = pd.read_csv(args.habitat, sep='\t',header=None)
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

# the same function in another way
'''
def store_habitat(args):
    #import lzma
    #habitat_dict = {}
    #with open(args.habitat,"rt") as f:
    #    for line in f:
    #        seq,env = line.strip().split("\t")
    #        habitat_dict[seq] = env
    #print(habitat_dict)

    ref_habitat = pd.read_csv(args.habitat, sep='\t',header=None)
    ref_habitat.columns = ['smorf','env']
    habitat_dict = dict(zip(ref_habitat['smorf'],ref_habitat['env']))
    return habitat_dict

def map_env(args):
    from os import path
    
    habitat_dict = store_habitat(args)
    result_file = path.join(args.output,"diamond.out.smorfs.tsv")
    habitat_mapped_file = path.join(args.output,"habitat.out.smorfs.tsv") 
    smorf_habitat = {}
    with open(habitat_mapped_file,"wt") as out:
        with open(result_file,"rt") as f:
            for line in f:
                linelist = line.strip().split("\t")
                if linelist[0] not in smorf_habitat.keys():
                    smorf_habitat[linelist[0]] = []
                smorf_habitat[linelist[0]].append(habitat_dict[linelist[3]])
        for key,value in smorf_habitat.items():
            value = ','.join(list(set(','.join(value).split(','))))
            out.write(f'{key}\t{value}\n')
'''
