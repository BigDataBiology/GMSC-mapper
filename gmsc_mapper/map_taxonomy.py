from os import path
import pandas as pd

def smorf_taxonomy(taxfile,resultfile,tmpdirname):
    print('Start taxonomy mapping...')
    taxonomy_file = path.join(tmpdirname,"taxonomy.out.smorfs.tmp.tsv") 
    
    result =  pd.read_csv(resultfile,sep="\t",header=None)
    result = result.rename(columns={0:'qseqid',1:'sseqid'})

    if taxfile.endswith('.gz'):
        reader =  pd.read_csv(taxfile,compression="gzip",sep="\t",chunksize=5000000,header=None)
    if taxfile.endswith('.xz'):
        reader =  pd.read_csv(taxfile,compression="xz",sep="\t",chunksize=5000000,header=None)
    if taxfile.endswith('.bz2'):
        reader =  pd.read_csv(taxfile,compression="bz2",sep="\t",chunksize=5000000,header=None)
    else:
        reader =  pd.read_csv(taxfile,sep="\t",chunksize=5000000,header=None)

    output_list = []
    for chunk in reader:
        chunk.columns = ['sseqid','taxonomy']
        output_chunk = pd.merge(result,chunk,how='inner')[['qseqid', 'sseqid','taxonomy']]
        output_list.append(output_chunk)
    output = pd.concat(output_list, axis=0).sort_values(by='qseqid')
    output.to_csv(taxonomy_file,sep='\t',index=False,header=False)
    print('Finish taxonomy mapping.')
    return taxonomy_file
    
def add_taxa_to_sseqid(taxa,og_tax,sseqid):
    taxa[sseqid] = []
    for tax in og_tax.split(";"):
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

def deep_lca(taxfile,outdirname,resultfile,tmpdirname):
    taxonomy_file = smorf_taxonomy(taxfile,resultfile,tmpdirname)
    taxonomy_dlca_file = path.join(outdirname,"taxonomy.out.smorfs.tsv")
    cluster = {}
    taxa = {}
    change = {}
    lastrank = ""
    og_tax = ""

    with open(taxonomy_dlca_file, "wt") as out:
        out.write(f'q_seqid\ttaxonomy\n')
        with open(taxonomy_file,"rt") as f:
            for line in f:
                linelist = line.strip().split("\t")
                qseqid = linelist[0]
                sseqid = linelist[1] 	

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

                if len(linelist) == 3:
                    og_tax = linelist[2]                
                    taxa = add_taxa_to_sseqid(taxa,og_tax,sseqid)
                else:
                    taxa[sseqid] = []
            compare_cluster(cluster,taxa,change,lastrank,out)
   
def taxa_summary(outdir):
    taxonomy_dlca_file = path.join(outdir,"taxonomy.out.smorfs.tsv")
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