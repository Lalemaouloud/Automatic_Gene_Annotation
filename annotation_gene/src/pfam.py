import requests
import xml.etree.ElementTree as ET



import requests

def pfam(Uniprot_id, output_file):
    """Find PFAM IDs for a list of UniProt IDs.

    Args:
        Uniprot_ids (list): A list of UniProt IDs.
    """
    print("\tPFAM IDs...")

    # Base URL for the EBI API request
    base_url = "https://www.ebi.ac.uk/proteins/api/proteins/"
    
    # Initialize an empty list to store PFAM IDs for the current UniProt ID
    pfam_ids = []
    
    for ID in Uniprot_id:
        # Construct the request URL for the current UniProt ID
        request_url = f"{base_url}{ID}"
        
        try:
            # Make the HTTP GET request
            response = requests.get(request_url, headers={"Accept": "application/json"})
            response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX or 5XX
            
            # Parse the JSON response
            data = response.json()
            
            # Initialize an empty list to store PFAM IDs for the current UniProt ID
            pfam_ids = []
            
            # Extract PFAM IDs from the JSON response
            for ref in data.get('dbReferences', []):
                if ref.get('type') == 'Pfam':
                    pfam_ids.append(ref.get('id'))
            
        
        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error for UniProt ID {ID}: {err}")
        except ValueError as parse_err:
            print(f"JSON Parsing Error for UniProt ID {ID}: {parse_err}")
        except Exception as e:
            print(f"An error occurred for UniProt ID {ID}: {e}")
        # Write Pfam IDs and Graphical view in HTML table
    output_file.write('<td><div class="scroll">')
    if pfam_ids != []:
        for ID in pfam_ids:
            link = f"<a href='https://pfam.xfam.org/family/{ID}'>{ID}</a>"
            g_url = f"https://pfam.xfam.org/family/{ID}#tabview=tab1"
            g_link = f"<a href='{g_url}'>Graphical view</a>"
            output_file.write(f'{link}: {g_link}<br>')
    else :
        output_file.write(f'Data not found un pfam<br>')
    output_file.write("</div></td>")









