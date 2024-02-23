from Bio import Entrez
import re
import json
import sys


def ncbi_gene_id(gene, organism, output_file):


    print('\tNCBI...')

    # Request with ESearch
    Entrez.email = 'lale.maouloud@univ-rouen.fr'
    term = f"({gene}[Gene Name]) AND {organism}[Organism]"
    handle = Entrez.esearch(db="Gene", term=term, retmax='20')
    records = Entrez.read(handle)
    gene_id = str(records['IdList'][0])

    # Extract the NCBI Gene ID and the Official Gene Name with EFetch
    handle = Entrez.efetch(db="Gene", id=gene_id,
                           rettype="docsum", retmode='json')
    record = json.loads(handle.read())
    temp_id = record['result']['uids'][0]
    official_name = record['result'][temp_id]['description']

    # Write the Official Gene Name in the HTML table
    output_file.write("<td><div class='scroll'>")
    output_file.write(official_name)
    output_file.write("</div></td>")

    # Write the NCBI Gene ID in the HTML table
    output_file.write("<td><div class='scroll'>")
    url = f"https://www.ncbi.nlm.nih.gov/gene/{gene_id}"
    output_file.write(f"<a href='{url}'>{gene_id}</a>")
    output_file.write("</div></td>")

    return gene_id


def refseq(gene_id, output_file):
    Entrez.email = "maellouis@protonmail.com"

    gene_search = Entrez.efetch(db="gene", id=gene_id,retmode="xml")
    try:
        gene_record = Entrez.read(gene_search)
        gene_record_txt=str(gene_record[0]['Entrezgene_locus'][0]['Gene-commentary_products'])
        gene_data=gene_record[0]['Entrezgene_locus'][0]['Gene-commentary_products']
        peptide_ID=[]
        transcript_id=[]
        for gene_entry in gene_data:
            if 'Gene-commentary_products' in gene_entry:
                for product_entry in gene_entry['Gene-commentary_products']:
                    if 'Gene-commentary_accession' in product_entry:
                        peptide_ID.append(product_entry['Gene-commentary_accession'])


        for record in gene_data:
            transcript_id.append(record['Gene-commentary_accession'])
       
         # Write the RefSeq RNA IDs in the HTML table
        output_file.write("<td><div class='scroll'>")
        if len(transcript_id)>0:
            for rna_id in transcript_id:
                if re.match('.M_', rna_id):  # Write only the conform IDs
                    link = f"https://www.ncbi.nlm.nih.gov/nuccore/{rna_id}"
                    output_file.write(f"<a href='{link}'>{rna_id}</a><br>")
        else:  # If no ID written, write No data found
            output_file.write('<i>No data found in NCBI databases</i>')
        output_file.write("</div></td>")

        
        # Write the RefSeq Protein IDs in the HTML table
        output_file.write("<td><div class='scroll'>")
        if len(peptide_ID)>0:
            for prot_id in peptide_ID:
                if re.match('.P_', prot_id):  # Write only the conform IDs
                    link = f"https://www.ncbi.nlm.nih.gov/protein/{prot_id}"
                    output_file.write(f"<a href='{link}'>{prot_id}</a><br>")
        else:
            output_file.write('<i>No data found in NCBI Databases</i>')
        output_file.write("</div></td>")


    except RuntimeError as e:
        print ("An error occurred while retrieving the annotations.")
        print ("The error returned was %s" % e)
        sys.exit(-1)


def main_NCBI(gene, organism, output_file):
    geneID_NCBI=ncbi_gene_id(gene, organism, output_file)
    refseq(geneID_NCBI,output_file)
    return geneID_NCBI
