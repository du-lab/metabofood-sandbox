# Author: Xiuxia Du
# 2024-07-25

import os

# set up directories
src_dir = os.getcwd()
data_dir = '../../data'
results_dir = '../../results'

# specify input files
kegg_id_file_name = 'Taxonomy_FullDataSet_2021-10-08.xlsx'
kegg_id_file_full_name = os.path.join(data_dir, kegg_id_file_name)

# workflow control
bool_retrieve_pathway_from_reactome = True
