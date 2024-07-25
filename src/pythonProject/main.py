# Author: Xiuxia Du
# 2024-07-25

import config

from retrieve_pathway_from_reactome import RetrievePathwayFromReactome

def main():
    if config.bool_retrieve_pathway_from_reactome:
        retrieve_pathway_from_reactome_obj = RetrievePathwayFromReactome()
        retrieve_pathway_from_reactome_obj.run()

if __name__ == "__main__":
    main()