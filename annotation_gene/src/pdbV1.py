import requests
import re

def fetch_pdb_ids(organism, gene, output_file):
    """
    Fetches PDB IDs for a given gene and organism from the UniProt API.

    Parameters:
    - organism: The name of the organism (e.g., "Homo sapiens").
    - gene: The gene symbol (e.g., "RAD51").

    Returns:
    A list of PDB IDs associated with the gene in the specified organism. Returns ["None"] if no PDB IDs are found.
    """
    print('\tPDB...')
    # Replace spaces in the organism name with '%20' for URL encoding
    organism_encoded = re.sub("_", "%20", organism)
    
    # Construct the request URL
    request_url = f"https://www.ebi.ac.uk/proteins/api/proteins?offset=0&size=100&gene={gene}&organism={organism_encoded}"
    
    # Send the GET request
    response = requests.get(request_url, headers={"Accept": "application/json"})
    
    # Check if the request was successful
    if not response.ok:
        print("Error fetching data")
        return []
    
    # Parse the JSON response
    data = response.json()
    
    # Initialize a list to hold PDB IDs
    pdb_ids = []
    
    # Loop through the dbReferences section to find PDB IDs
    for entry in data:
        for reference in entry.get("dbReferences", []):
            if reference["type"] == "PDB":
                pdb_ids.append(reference["id"])
                


    output_file.write('<td><div class="scroll">')
    if pdb_ids != []:
        for ID in pdb_ids:
            link = f"<a href='https://www.rcsb.org/structure/{ID}'>{ID}</a>"
            g_url = f"https://www.rcsb.org/3d-view//{ID}#tabview=tab1"
            g_link = f"<a href='{g_url}'>Graphical view</a>"
            output_file.write(f'{link}: {g_link}<br>')
        output_file.write("</div></td>")
    else:
        output_file.write("<i>No data in the PDB database</i>")
    output_file.write("</div></td>")
