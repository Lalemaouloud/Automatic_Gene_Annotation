import re
import requests

def uniprot(gene, organism, output_file):
    """Search for the UniProtKB ID(s).
The function Uniprot_fct takes three arguments: specie (organism name), i (gene identifier), and output_file (HTML file object where the output will be written).
It first converts the organism name to a format suitable for use in a URL by replacing spaces with "%20".
Then it constructs a URL for the API request to retrieve protein data from UniProt, including the gene identifier and species information.
It sends a GET request to the UniProt API using the constructed URL.
If the request is successful, it parses the JSON response.
It checks if the response contains protein data.
If protein data is present, it extracts the UniProt accession ID and official protein name(s).
It writes the UniProt ID as a hyperlink and the official protein name(s) to the output HTML file.
If there is no response or if protein data is not found, it writes a message indicating no data found in the output HTML file.
Finally, it returns the UniProt ID or None, depending on whether protein data was found or not.
    """
    print('\tUniprot...')
    # Convert organism name to a format suitable for use in a URL
    specie_uniprot = re.sub("_", "%20", organism)
    
    uniprot_accessions=Uniprot_accession(organism,gene)
    uniprot_names=Uniprot_fullname(organism,gene)
    

      

        # Write the UniProt ID as a link in the output HTML file
    output_file.write("<td><div class='scroll'>")
    for k in range(len(uniprot_accessions)): 
        URL = "https://www.uniprot.org/uniprotkb/"+uniprot_accessions[k]+"/entry"
        output_file.write(f'<a href="{URL}/{uniprot_accessions[k]}">{uniprot_accessions[k]}</a><br>')
    output_file.write("</div></td>")

        # Write the UniProt official name(s) in the output HTML file
    output_file.write("<td><div class='scroll'>")
    for k in range(len(uniprot_accessions)): 
        output_file.write(f'{uniprot_names[k]}</br>')
    output_file.write("</div></td>") 
        # Return the UniProt ID
    return uniprot_accessions




def Uniprot_Requete(specie, i):
	specie_uniprot=re.sub("_", "%20", specie)
	requestURL = "https://www.ebi.ac.uk/proteins/api/proteins?offset=0&size=100&gene="+i+"&organism="+specie_uniprot
	r = requests.get(requestURL, headers={ "Accept" : "application/json"})
	if not r.ok:
	  print("erreur")
	responseBody = r.json()

		
	return responseBody


def Uniprot_accession(specie,i):
	uniprot_accessions=[]
	requete=Uniprot_Requete(specie,i)
	expression_reguliere = re.compile(r"\b" + re.escape(i) + r"\b", re.IGNORECASE)
	for j in range(len(requete)):
		if expression_reguliere.search(requete[j]["gene"][0]["name"]["value"]):
			uniprot_accessions.append(requete[j]["accession"])
	return(uniprot_accessions)
	
	
	
def Uniprot_fullname(specie,i):
	uniprot_fullnames=[]
	uni_requete=Uniprot_Requete(specie,i)
	expression_reguliere = re.compile(r"\b" + re.escape(i) + r"\b", re.IGNORECASE)
	for j in range(len(uni_requete)):
		if expression_reguliere.search(uni_requete[j]["gene"][0]["name"]["value"]):
			if uni_requete[j]["protein"].get("recommendedName"):
				uniprot_fullnames.append(uni_requete[j]["protein"]["recommendedName"]["fullName"]["value"])
			elif uni_requete[j]["protein"].get("submittedName"):
				uniprot_fullnames.append(uni_requete[j]["protein"]["submittedName"][0]["fullName"]["value"])
	return uniprot_fullnames




