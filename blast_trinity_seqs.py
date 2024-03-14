from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

import re

def nr_blast():

    examined_file = 'IVF_MIM_novel.fasta'
    fasta = open(examined_file).read()
    result_handle = NCBIWWW.qblast("blastn", "nt", fasta)

    with open('nr_output.xml', 'w') as save_file:
        blast_results = result_handle.read()
        save_file.write(blast_results)

def est_blast():

    examined_file = 'nr_blast_out_headers.fasta'
    fasta = open(examined_file).read()
    result_handle = NCBIWWW.qblast("blastn", "est", fasta)

    with open('est_output.xml', 'w') as save_file:
        blast_results = result_handle.read()
        save_file.write(blast_results)



def parse_blast_results(result_to_parse):
    result_handle = open(result_to_parse)
    blast_records = NCBIXML.parse(result_handle)

    print("query","@", "al_title",'@',"al_accession","@","evalue")

    for blast_record in blast_records:
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                if p.search(str(alignment.title)):
                    pass
                else:
                    #print(blast_record.query,"@", alignment.title,"@", alignment.accession,"@", hsp.expect)
                    print(alignment.accession)






#nr_blast()

p = re.compile('chromosome')
#parse_blast_results('nr_output.xml')

est_blast()