import pandas as pd
import numpy as np
import os
import csv


def wrangle(filename):
    dataframe = pd.read_csv(filename)
    
    # counting proteins from specific group (BIN_1)
    blastx_contains = dataframe[dataframe['sprot_Top_BLASTX_hit'].str.contains('Teleostei')]
    blastp_contains = dataframe[dataframe['sprot_Top_BLASTP_hit'].str.contains('Teleostei')]

    blastx_blastp_merged = pd.merge(blastx_contains, blastp_contains, how='outer')

    without_duplicates = blastx_blastp_merged.drop_duplicates(['#gene_id'])
    print(without_duplicates['#gene_id'].count())
    
    # counting transcripts not recognized as proteins (BIN_3)
    blastx_match = dataframe[dataframe['sprot_Top_BLASTX_hit'] == '.']
    blastp_match = dataframe[dataframe['sprot_Top_BLASTP_hit'] == '.']
    
    merged = pd.merge(blastx_match, blastp_match) # default how='inner': Use only the key combinations observed in both tables. jesli byloby 'outer' to lapalby tez pojedyncze '.' w wierszach, gdzie tylko jedna z kolumn jest '.'
    merged['#gene_id'].count()

    without_dup2 = merged.drop_duplicates(['#gene_id'])
    print(without_dup2['#gene_id'].count())
    
    without_dup2.to_csv('output.csv')

def get_headers(output_file):
    dataframe = pd.read_csv(output_file)
    
    get_headers = dataframe['transcript_id']
    
    get_headers.to_csv('unannotated_headers.csv', index = False)

#def grab_fasta(unannotated_headers):
#    with open(unannotated_headers, 'r') as csvfile:
#        lines = csv.reader(csvfile)
#        
#        for line in lines:
#            #print(line[0])
#            sequence = os.system('samtools faidx ' + line[0] + ' -o annotated.fasta')
#        
#        #print(sequence)



#wrangle('trinotate_annotation_report.csv')
#get_headers('unannotated.csv')
        
grab_fasta('unannotated_headers.csv')


