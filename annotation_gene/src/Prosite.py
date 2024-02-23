import requests
import re


def Uniprot_Requete(organism,gene):
	specie_uniprot=re.sub("_", "%20", organism)
	requestURL = "https://www.ebi.ac.uk/proteins/api/proteins?offset=0&size=100&gene="+gene+"&organism="+specie_uniprot
	r = requests.get(requestURL, headers={ "Accept" : "application/json"})
	if not r.ok:
	  print("erreur")
	responseBody = r.json()
	return responseBody






#on recupere les ID Prosite
def Get_Prosite_id(organism,gene):
	print('\tProsite...')
	PROSITE_ids=[]
	j=-1
	uni_requete=Uniprot_Requete(organism,gene)
	while j+1 < len(uni_requete[0]["dbReferences"]):
			j+=1
			if uni_requete[0]["dbReferences"][j]["type"]=="PROSITE" :
				PROSITE_ids.append(uni_requete[0]["dbReferences"][j]["id"])
	if PROSITE_ids == [] :
		PROSITE_ids.append("None")
	return PROSITE_ids	


#A mettre en clicable sur le nom
def Prosite_id_url (PROSITE_ids):
	prosite_ids_url=[]
	if PROSITE_ids != ["None"] :
		for prosite_id in PROSITE_ids :
			
			prosite_ids_url.append("https://prosite.expasy.org/"+prosite_id)
	else :
		prosite_ids_url=["None"]
	return prosite_ids_url

#Verifier qu'un url est bon : pour graph views
def Verifier_url(url):
    try:
        reponse = requests.get(url, timeout=10)
        if reponse.status_code == 200:
            contenu = reponse.text
            if "ERROR: no hit!" in contenu:
                return False
            else:
                return True
        else:
            return False
    except requests.ConnectionError:
        return False



def generate_protein_motif_info(organism, gene, output_file):
    """
    Fetches, processes, and outputs protein motif information into a given HTML file.

    Parameters:
    - organism: The name of the organism.
    - gene: The gene of interest.
    - output_file: An open file handle for the output HTML file.
    """
    prosite_ids = Get_Prosite_id(organism, gene)
    prosite_ids_url = Prosite_id_url(prosite_ids)
    graphs_url = []

    for prosite in prosite_ids:
        url = f"https://prosite.expasy.org/cgi-bin/prosite/PSView.cgi?ac={prosite}"
        if Verifier_url(url):
            graphs_url.append(url)
        else:
            graphs_url.append("None")

    # Writing to HTML
    output_file.write("<td><div class='scroll'>\n")
    if prosite_ids != ["None"]:
        for id, graph_url in zip(prosite_ids, graphs_url):
            # Assuming domain is predefined or obtained from somewhere
            domain = "https://prosite.expasy.org"
            url = f"{domain}/{id}"
            output_file.write(f'<a href="{url}">{id}</a>\n')

            if graph_url != "None":  # If a valid graphical view URL is available
                link = f": <a href='{graph_url}'>Graphical view</a>"
                output_file.write(link + "<br>\n")
            else:
                output_file.write("<br>\n")
    else:
        output_file.write("<i>No data found in Protiste database</i>\n")
    output_file.write("</div></td>\n")
