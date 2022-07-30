# how to solve memory/time consuming
# adapt to different format(.xz .gz)
from os import path
import pandas as pd

def smorf_taxonomy(args,resultfile,tmpdirname):
    taxonomy_file = path.join(tmpdirname,"taxonomy.out.smorfs.tmp.tsv")	

    result = pd.read_csv(resultfile, sep='\t',header=None)
    result.columns = ['qseqid','full_qseq','qlen','sseqid','full_sseq','slen','pident','length','evalue','qcovhsp','scovhsp']
    ref_taxonomy = pd.read_csv(args.taxonomy, sep='\t',header=None)
    ref_taxonomy.columns = ['sseqid','taxonomy']

    output = pd.merge(result,ref_taxonomy,how='left')[['qseqid', 'sseqid','taxonomy']]
    output.to_csv(taxonomy_file,sep='\t',index=False)
    return taxonomy_file

def add_taxa_to_sseqid(taxa,linelist,original_tax,sseqid):
    taxa[sseqid] = []
    if len(linelist) == 3:
        for tax in original_tax.split(";"):
            taxa[sseqid].append(tax)
    return(taxa)

def compare_cluster(cluster,taxa,change,lastrank,out):
    for q_seqid,s_seqid_list in cluster.items():
        change[q_seqid] = []
        for rank in range(7):
            flag = 1
            for s_seqid in s_seqid_list:
                if taxa[s_seqid]: # If a sequence has taxonomy
                    if len(taxa[s_seqid]) >= rank+1: #If a sequence has enough taxonomy to compare,if blank,continue
                        if lastrank == "":
                            lastrank = taxa[s_seqid][rank]
                        else:
                            if taxa[s_seqid][rank] != lastrank: #If the current taxonomy is same as last one
                                flag = 0
                                lastrank = ""
                                break
                            else:
                                continue
                    else:   
                        continue
                else:  
                    continue
            if flag == 1: #add same taxonomy every rank
                if lastrank != "":
                    change[q_seqid].append(lastrank)
                    lastrank = ""
                else: #for sequence which doesn't have taxonomy
                    lastrank = ""
                    break
            else:
                break  
        if change[q_seqid]: #after all rank circle,write results       
            taxonomy = ";".join(change[q_seqid])
            out.write(f'{q_seqid}\t{taxonomy}\n')
        else: #for sequence which doesn't have taxonomy
            out.write(f'{q_seqid}\n')     

def deep_lca(args,resultfile,tmpdirname):
    taxonomy_file = smorf_taxonomy(args,resultfile,tmpdirname)
    taxonomy_dlca_file = path.join(args.output,"taxonomy.out.smorfs.tsv")
	
    cluster = {}
    taxa = {}
    change = {}
    lastrank = ""

    with open(taxonomy_dlca_file, "wt") as out:
        with open(taxonomy_file,"rt") as f:
            for line in f:
                linelist = line.strip().split("\t")
                qseqid = linelist[0]
                sseqid = linelist[1] 	
                if len(linelist) == 3:
                    original_tax = linelist[2]

                if cluster:
                    if qseqid in cluster.keys():
                        cluster[qseqid].append(sseqid)
                    else:
                        compare_cluster(cluster,taxa,change,lastrank,out)             
                        cluster = {}
                        taxa = {}
                        change = {}
                        cluster[qseqid] = [sseqid]
                else:
                    cluster[qseqid] = [sseqid]
                
                taxa = add_taxa_to_sseqid(taxa,linelist,original_tax,sseqid)
            compare_cluster(cluster,taxa,change,lastrank,out)                                            

def taxa_summary(args):
    taxonomy_dlca_file = path.join(args.output,"taxonomy.out.smorfs.tsv")
    output = pd.read_csv(taxonomy_dlca_file, sep='\t')
    rank = {1:'kingdom',2:'phylum',3:'class',4:'order',5:'family',6:'genus',7:'species',8:'no rank'}
    number_dict = dict(output['taxonomy'].fillna(';;;;;;;').apply(lambda x: len(x.split(';'))).value_counts())
    number_dict_percentage = dict(output['taxonomy'].fillna(';;;;;;;').apply(lambda x: len(x.split(';'))).value_counts(normalize=True))
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
    return annotated_number,rank_number,rank_percentage



'''
def store_taxonomy(args):
    import lzma
    taxonomy_dict = {}
    with open(args.taxonomy,"rt") as f:
        for line in f:
            linelist = line.strip().split("\t")
            if len(linelist) == 2:
                taxonomy_dict[linelist[0]] = linelist[1]
            else:
                taxonomy_dict[linelist[0]] = ""
    return taxonomy_dict

def map_taxonomy(args):
    taxonomy_dict = store_taxonomy(args)
    result_file = path.join(args.output,"diamond.out.smorfs.tsv")
    taxonomy_mapped_file = path.join(args.output,"taxonomy.out.smorfs.tsv")

    with open(taxonomy_mapped_file,"wt") as out:
        with open(result_file,"rt") as f:
            for line in f:
                line = line.strip()
                linelist = line.split("\t")
                taxa = taxonomy_dict[linelist[3]]
                out.write(f'{line}\t{taxa}\n') 
'''			