import pandas as pd
import pdf2doi
import requests
import bibtexparser


# get DOI from file
def get_doi_from_file(filenamepath):
    source_info = pdf2doi.pdf2doi(filenamepath)
    return source_info["identifier"]


# get publication metadata from DOI
def get_metadata_from_doi(doi):
    # URL for the DOI system
    url = f"https://doi.org/{doi}"
    
    # Headers to request the BibTeX format
    headers = {
        'Accept': 'text/bibliography; style=bibtex',
    }
    
    # Make the GET request
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        
        # Load the BibTeX data
        bib_database = bibtexparser.loads(response.text)
        
        # Assuming the first entry is the one we want to extract information from
        entry = bib_database.entries[0]
        
        # Extract relevant fields
        author = entry.get('author', 'No author found')
        journal = entry.get('journal', 'No journal found')
        year = entry.get('year', 'No publication year found')
        title = entry.get('title', 'No publication year found')
        return {
            'Author': author,
            'Journal': journal,
            'Year': year,
            'Title': title,
        }

    else:
        return {
            'Author': "not found (error)",
            'Journal': "not found",
            'Year': "not found",
            'Title': "not found"
        }



# return metadata from sources as df or md
def sources(answer, format="df"):
    sources_df = pd.DataFrame()
    sources_md = "\n\nLocal Sources:\n"

    # iterate through each source of the answer
    for source in range(len(answer["source_documents"])):

        # extract metadata
        source_raw = answer["source_documents"][source].metadata.copy()

        # get metadata
        source_doi = get_doi_from_file(source_raw["source"])
        source_metadata = get_metadata_from_doi(source_doi)

        # only show filename and subfolders of the folder "Referenzen"
        source_raw["source"] = source_raw["source"].split("Referenzen\\")[1]

        # concat to df
        source_df = pd.DataFrame([source_metadata | source_raw])
        sources_df = pd.concat([sources_df, source_df], axis=0)

        # format to markdown
        source_md = f"- {source_metadata['Author']}. *{source_metadata['Title']}.* {source_metadata['Journal']}, {source_metadata['Year']}. Local file: {source_raw['source']}, page {source_raw['page']}.\n" 
        sources_md += source_md

    # define output format
    if format == "df":
        output = sources_df
    elif format == "md":
        output = sources_md
    else:
        print("unknown output format")

    return output
