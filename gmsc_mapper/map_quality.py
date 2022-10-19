from os import path
import pandas as pd

def smorf_quality(outdir,qualityfile,resultfile):
    quality_file = path.join(outdir,"quality.out.smorfs.tsv")	

    result = pd.read_csv(resultfile,sep='\t',header=None)
    result = result.rename(columns={0:'qseqid',1:'sseqid'})
    if qualityfile.endswith('.gz'):
        ref_quality =  pd.read_csv(qualityfile,compression="gzip",sep='\t',header=None)
    if qualityfile.endswith('.xz'):
        ref_quality =  pd.read_csv(qualityfile,compression="xz",sep='\t',header=None)
    if qualityfile.endswith('.bz2'):
        ref_quality =  pd.read_csv(qualityfile,compression="bz2",sep='\t',header=None)
    else:
        ref_quality =  pd.read_csv(qualityfile,sep="\t",header=None)

    ref_quality.columns = ['sseqid']
    ref_quality['quality'] = 'high quality'

    output = pd.merge(result,ref_quality,how='left')[['qseqid', 'quality']].fillna('low quality')
    output = output.groupby('qseqid',as_index=False,sort=False).agg({'quality':lambda x : ','.join(x.drop_duplicates())})
    rule = {"high quality":0,"low quality":1}
    output['quality'] = output['quality'].apply(lambda x: sorted(x.split(','),key=lambda x:rule[x])[0])

    number_dict = dict(output['quality'].value_counts())
    number_dict_normalize = dict(output['quality'].value_counts(normalize=True))
    if "high quality" in number_dict.keys():
        number = number_dict['high quality']
        percentage = number_dict_normalize['high quality']
    else:
        number = 0
        percentage = 0
    output.to_csv(quality_file,sep='\t',index=False)
    return number,percentage