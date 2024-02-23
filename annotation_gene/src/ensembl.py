import requests, sys, json, re
  
server = "https://rest.ensembl.org"

def ens_db(organism, gene,output_file):

    print('\tEnsembl...')
    # Changer le nom d'espèce pour les bactéries : il faut un nom de souche obligatoirement
    # Par défaut si aucune souche n'est mentionnée (si il n'y a qu'un _) alors on récupère le 1er nom de souche listé dans URL_name
    organism_real=organism
    if getGenomeBrowser(organism) == "EnsemblBacteria" and organism.count("_") == 1:
        organism = getSoucheBacteria(organism)

    # Récupération du GeneId
    ens_ID = getGeneId(organism, gene)

    # Genome Browser : la construction d'URL est différente pour les bactéries, les vertébrés et les autres
    ens_URL="Data not found in Ensembl"
    if getGenomeBrowser(organism_real) == "EnsemblVertebrates":
        ens_URL = "https://ensembl.org/" + organism + "/Location/View?;g=" + ens_ID
    elif getGenomeBrowser(organism_real) == "EnsemblBacteria":
        ens_URL = "https://bacteria.ensembl.org/" + organism + "/Gene/Summary?g=" + ens_ID
    else:
        divison = re.sub("Ensembl", "", getGenomeBrowser(organism_real))
        ens_URL = "https://" + divison + ".ensembl.org/" + organism + "/Gene/Summary?g=" + ens_ID + ";db=core"

    #write geneID
    output_file.write('<td><div class="scroll">')
    # Write in HTML table the linkable ID
    output_file.write(f"<a href={ens_URL}>{ens_ID}</a>")
    output_file.write('</div></td>')



    #Construction d'URL pour transcrits et protéines : utilisation d'un dictionnaire
    dic = {
        'EnsemblBacteria': 'bacteria.ensembl.org',
        "EnsemblFungi": 'fungi.ensembl.org',
        'EnsemblVertebrates': 'ensembl.org',
        'EnsemblPlants': 'plants.ensembl.org'
    }

    server = "https://rest.ensembl.org"
    ext = f"/info/genomes/{organism}?"
    headers = {"Content-Type": "application/json"}
    r = requests.get(server+ext, headers=headers)

    if not r.ok:  # If species not found
        ens_url_tr = "0"
    else:
        decoded = r.json()
        if decoded["division"] in dic:  # Extract domain from request
            ens_url_tr = dic[decoded['division']]  # Extract domain from dic
        else:
            ens_url_tr = "0"
            
    # Récupération des transcrits et protéines
    transcrits = getTranscripts(organism, gene)

    # Write the transcript IDs in the HTML table
    output_file.write('<td><div class="scroll">')
    if transcrits != "Data not found":
        for transcrit in transcrits:
            var = "Transcript/Summary?t"
            url = f"https://{ens_url_tr}/{organism}/{var}={transcrit['id']}"
            output_file.write(f"<a href={url}>{transcrit['id']}</a><br>")
    else :
        output_file.write("<i>Data not found in Ensembl</i><br>")
    output_file.write('</div></td>')

    # Write the protein IDs in the HTML table
    output_file.write('<td><div class="scroll">')
    if transcrits != "Data not found":
        for prot in transcrits:
            if "Translation" in prot:
                var = "Transcript/ProteinSummary?g"
                url = f"https://{ens_url_tr}/{organism}/{var}={ens_ID};t={prot['Translation']['id']}"
                output_file.write(f"<a href={url}>{prot['Translation']['id']}<br></a>")
            else :
                output_file.write("<i>Data not found in Ensembl</i><br>")
    else :
        output_file.write("<i>Data not found in Ensembl</i><br>")
    output_file.write('</div></td>')

    # Récupération des orthologues :
    # Si aucun orthologue n'est listé (si la liste data est vide) alors on retourne "None"
    # C'est le cas pour les bactéries
    homologies = getOrthologues(organism, ens_ID)


 # Write Ortholog links from IDs in the HTML table
    output_file.write('<td><div class="scroll">')
    if homologies != "Data not found" :
        var = "Gene/Compara_Ortholog?db=core;g"
        url = f"https://{ens_url_tr}/{organism}/{var}={ens_ID}"
        output_file.write(f"<a href={url}>Orthologs list</a><br>")
        for ortho in homologies:
            output_file.write(f"{ortho['target']['id']}<br>")
    else :
        output_file.write("<i>Data not found in Ensembl</i><br>")
    output_file.write('</div></td>')









#on doit faire des requetes, pour eviter de toujours retaper la requete on la place dans une fonction
def sendRequest(request):
	r = requests.get(server+request, headers={ "Content-Type" : "application/json"})
	if not r.ok:
		return("Not found")
		#r.raise_for_status()
		#sys.exit()
	else :
		return r.json()

#pour certaines requetes il faut renseigner une souche bactérienne
def getSoucheBacteria(organism):
	request="/info/genomes/taxonomy/"+organism
	return sendRequest(request)[0]["url_name"]

#recuperer le gene Id
def getGeneId(organism, gene):
    request = "/lookup/symbol/" + organism + "/" + gene +"?expand=1"
    result=sendRequest(request)
    if result == "Not found":
         return "Data not found"
    else :
        return sendRequest(request)['id'] 

#recuperer les transcripts Id
def getTranscripts(Gene_espece, gene):
	request = "/lookup/symbol/" + Gene_espece +"/"+ gene+"?expand=1"
	result=sendRequest(request)
	if result == "Not found":
		return "Data not found"
	else :
		return sendRequest(request)['Transcript'] 

#recuperer les orthologues
def getOrthologues(organism, geneId):
	request = "/homology/id/" + organism + "/" + geneId + "?type=orthologues"
	result=sendRequest(request)
	if result == "Not found":
		return "Data not found"
	elif sendRequest(request)['data']!= []:
		return sendRequest(request)['data'][0]['homologies']
	else :
		return "Data not found"

#savoir à quelle famille appartient l espece (organisme)
def getGenomeBrowser(organism):
	request = "/info/genomes/taxonomy/"+organism+"?"
	result=sendRequest(request)
	if result == "Not found":
		return "Data not found"
	else :
		return sendRequest(request)[0]["division"]