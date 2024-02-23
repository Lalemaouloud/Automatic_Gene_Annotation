import requests
from src.Uniprot import *

def go(output_file, gene, organism):
    """Find features in the Go database from UniprotKB IDs.

    Find go features (molecular function, biological process and cellular
    component) of a protein, and write them in 3 columns of a HTML table.

    Args:
        uniprot_id (list)
        output_file (open file) : file to write in.
    """
    print('\tGo ...')

    go_ids = Uniprot_GO(organism, gene)
    go = {'function': {}, 'component': {}, 'process': {}}

    go_names = []
    go_aspect = []
    for go_id in go_ids:
        go_names.append(GO_name(go_id))
        go_aspect.append(GO_aspect(go_id))

    if go_names != "None":
        for nombre in range(len(go_aspect)):
            if go_aspect[nombre] == "biological_process":
                go["process"][go_ids[nombre]] = go_names[nombre]
            elif go_aspect[nombre] == "cellular_component":
                go["component"][go_ids[nombre]] = go_names[nombre]
            elif go_aspect[nombre] == "molecular_function":
                go["function"][go_ids[nombre]] = go_names[nombre]


    # Write each go feature in a different col
    for feature in go:
        output_file.write('<td><div class="scroll">')
        if go[feature] == {}:
            output_file.write('<i>No data found in GO database</i>')
        else:
            for id in go[feature]:
                goName = go[feature][id]
                link = f"http://amigo.geneontology.org/amigo/term/{id}"
                output_file.write(f'<a href={link}>{id}</a>: {goName}</a><br>')
        output_file.write('</div></td>')


#Recuperer le GO Id via requete Uniprot
def Uniprot_GO(organism,gene):
	j=-1
	GO_id=[]
	# Convert organism name to a format suitable for use in a URL
	specie_uniprot=re.sub("_", "%20", organism)
	uni_requete=Uniprot_Requete(specie_uniprot,gene)
	for k in range(len(uni_requete)):
		if uni_requete[k]["gene"][0]["name"]["value"] == gene : #il faut prendre les GO terms uniquement des bons accession (meme selection faite pour uniprot accession)
			while j+1 < len(uni_requete[k]["dbReferences"]):
				j+=1
				if uni_requete[k]["dbReferences"][j]["type"]=="GO" :
					GO_id.append(uni_requete[k]["dbReferences"][j]["id"])
	if GO_id == [] :
		GO_id.append("None")
	return GO_id

#Effectuer une requete GO
def GO_requete(go_id):
	go_id_requete=re.sub("_", "%20", go_id)
	requestURL = "https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/"+go_id_requete
	r = requests.get(requestURL, headers={ "Accept" : "application/json"})
	if not r.ok:
		print("erreur")	
	responseBody = r.json()
	return(responseBody)

#Recuperer les noms associes aux GO ID
def GO_name(go_id):
	if go_id == "None" :
		return "None"
	else :
		return GO_requete(go_id)["results"][0]["name"]

#Recuperer l aspect
def GO_aspect(go_id):
	if go_id == "None" :
		return "None"
	else :
		return GO_requete(go_id)["results"][0]["aspect"]