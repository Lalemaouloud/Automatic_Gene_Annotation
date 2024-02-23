
from src.ensembl import *
from src.table import init_table, init_row, end_table
from src.ncbi import *
from src.Uniprot import *
from src.pfam import *
from src.Prosite import generate_protein_motif_info
from src.GO import *
from src.kegg import kegg
from src.prot_string import string
from src.pdbV1 import *



def main(filename, txt):
    line_number = 1
    output_file = open("Results.html", "w")
    with open(filename, 'r') as gene_file:
        gene_content = gene_file.readlines()
    init_table(output_file)
    for line in gene_content:
        line=re.sub(" ", "_", line)
        txt_done(txt, line_number)
        gene, organism = init_row(line, output_file)

        # NCBI Done 
        txt_statut(txt, line_number, '    NCBI will be done soon...',)
        ncbi_main_id=main_NCBI(gene=gene,organism=organism,output_file=output_file)


        # Ensembl Done 
        txt_statut(txt, line_number, '   Ensembl will be done soon...',)
        ens_url = ens_db(organism,gene,output_file)

        # Uniprot Done 
        txt_statut(txt, line_number, '   UniProt will be done soon...',)
        Uniprot_id = uniprot(gene, organism, output_file)

        # String Done 
        txt_statut(txt, line_number, '   String prot will be done soon...',)
        string(Uniprot_id, output_file)

         # PDB a voir comment faire et pourquoi ids pas dans la liste
        txt_statut(txt, line_number, '   PDB will be done soon...',)
        fetch_pdb_ids(organism, gene, output_file)


        # Pfam Done
        txt_statut(txt, line_number, '   Pfam will be done soon...',)
        pfam(Uniprot_id, output_file)

        # Prosite done
        txt_statut(txt, line_number, '   Protsite will be done soon...',)
        generate_protein_motif_info(organism, gene, output_file)


        # KEGG Done 
        txt_statut(txt, line_number, '   KEGG will be done soon...',)
        kegg(ncbi_main_id, output_file)

        # Go
        txt_statut(txt, line_number, '   GO will be done soon...',)
        go(output_file, gene, organism)



        # End of the row
        output_file.write("</tr>")
        line_number += 1

    end_table(output_file, txt)


def txt_done(txt, line_number):
    """
    Add to the text widget 'Done and perfect' on the previous line
    """
    if line_number > 1:
        cursor = f"{line_number-1}.end"
        txt.tag_config("the execution is Finished", foreground="green")
        txt.insert(cursor, " Perfect and Done ", ('the execution is Finished '))
        txt.update()


def txt_statut(txt, line_number, step):
    """
    Write on the text widget the current task next to species
    """
    cursor = f"{line_number}.end"
    txt.tag_config("Current", foreground="#E95420")
    txt.insert(cursor, step, ('Current'))
    txt.update()
    txt.delete(f"{'Current'}.first", f"{'Current'}.last")


def txt_statut(txt, line_number, step):
    """
    Write on the text widget the current task next to species.
    """
    try:

        cursor = f"{line_number}.end"
        txt.tag_config("Current", foreground="#007BFF")  
        txt.tag_remove("Current", "1.0", "end")
        txt.insert(cursor, f" {step}", "Current")
        txt.see(cursor)
        
        txt.update()  # Update the widget to reflect changes immediately
        txt.delete(f"{'Current'}.first", f"{'Current'}.last")
        
    except Exception as e:
        print(f"Error updating text status: {e}")
