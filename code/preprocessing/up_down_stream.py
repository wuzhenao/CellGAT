import requests
import pandas as pd

# OmniPath API endpoint for interactions
OMNIPATH_API_URL = "https://www.omnipathdb.org/api/interactions"

def fetch_interactions():
    """
    Fetch interaction data from OmniPath API.
    """
    response = requests.get(OMNIPATH_API_URL)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def extract_upstream_downstream_genes(data):
    """
    Extract upstream and downstream genes from OmniPath data.
    """
    upstream_genes = set()
    downstream_genes = set()

    for interaction in data['interactions']:
        upstream_gene = interaction['source']
        downstream_gene = interaction['target']
        
        upstream_genes.add(upstream_gene)
        downstream_genes.add(downstream_gene)
    
    return upstream_genes, downstream_genes

def main():
    try:
        # Fetch the data
        data = fetch_interactions()
        
        # Extract the upstream and downstream genes
        upstream_genes, downstream_genes = extract_upstream_downstream_genes(data)
        
        # Convert to pandas DataFrame for better visualization
        upstream_df = pd.DataFrame(list(upstream_genes), columns=['Upstream Genes'])
        downstream_df = pd.DataFrame(list(downstream_genes), columns=['Downstream Genes'])
        
        # Output the results
        print("Upstream Genes:")
        print(upstream_df)
        
        print("\nDownstream Genes:")
        print(downstream_df)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
