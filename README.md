# Automated gene annotation program
Automated gene annotation program utilizing multiple APIs.



## Table of Contents

- [Table of Contents](#table-of-contents)
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Description

This program annotate the provided gene according to the provided specie
It uses APIs to work. The differents APIs used are the following:
- [Ensembl](https://rest.ensembl.org/)
- [Gene Onthology](https://api.geneontology.org/)
- [Kegg](https://www.kegg.jp/kegg/rest/)
- [NCBI - E-utilities](https://eutils.ncbi.nlm.nih.gov/)
- [PDBe](https://www.ebi.ac.uk/pdbe/pdbe-rest-api)
- [Pfam](https://www.ebi.ac.uk/proteins/api/doc/)
- [Prosite](https://prosite.expasy.org/scanprosite/scanprosite_doc.html)
- [String](https://string-db.org/help/api/)
- [Uniprot]( https://www.uniprot.org/help/api)

## Installation

To use this program, you need to install the following Python packages:

- [BioPython](https://biopython.org/) - Used for bioinformatics tasks (specific APIs and parsing).


- [Requests](https://fr.python-requests.org/) - Used for making HTTP requests.

Using pip:
```bash
pip install biopython requests
```
You can also use conda if you want:
```bash
conda install biopython requests
```
*Make sure you are inside a conda environement*

For the app, open a terminal and copy/paste :

```bash
git clone https://gitea.maeltech.cc/Drelioss/annotation_gene.git
cd annotation_gene
python3 app.py
```

# Usage

To use this application launch the "app.py" file:
```bash
python3 app.py
```

Then, when you click on the "Insert File" button, the program will ask you to choose a file.

**Your file must be a text file with the following syntax:**

GENENAME1,specie1

GENENAME2,specie2


**⚠️** You can only load one file at a time and the type-in feature isn't supported for now



Then click on "Execute" and the program will launch. You will have a return of what is actually be done side to the files in the preview box

When it has finished it prints you: "Done and PErfect in the console" next to the last entry and the text will turn green.

You can then view the result file by clicking "Open Results"

To safely close the program once finished you can close the window (graphically or with "Alt. + f4")

# License

MIT License

Copyright (c) [2024]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
