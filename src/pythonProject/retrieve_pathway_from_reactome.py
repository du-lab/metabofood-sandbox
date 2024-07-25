# Author: Xiuxia Du
# Date: 2024-07-24

import pandas as pd
import os
import requests
import json

import config
class RetrievePathwayFromReactome:

    def get_compounds(self):
        data_in_df = pd.read_excel(config.kegg_id_file_full_name,
                                   sheet_name='TaxonomyOrderCleanFood',
                                   engine='openpyxl', )
        compound_df = data_in_df.loc[:, ['Compound Name From Literature', 'INCHI Key', 'kegg_id']]

        tf = compound_df['kegg_id'].isna()
        compound_to_consider_df = compound_df.loc[~tf, :]
        kegg_id_list = compound_to_consider_df['kegg_id'].to_list()
        return kegg_id_list

    def get_reactome_pathway_for_one_compound(self, kegg_id):
        url = 'https://reactome.org/ContentService/references/mapping/' + kegg_id
        headers = {'accept': 'application/json'}
        response = requests.get(url, headers=headers)

        json_file_id = response.text
        code_response = response.status_code

        if code_response != 404:
            returned_id_list = json.loads(json_file_id)

            pathway_result_df = pd.DataFrame(columns=['KEGG ID', 'compound name', 'formula', 'dbId', 'pathway name', 'stId',
                                                      'isInDisease', 'speciesName'])

            for cur_returned_id in returned_id_list:
                dbid = cur_returned_id['dbId']
                formula = cur_returned_id['formula']

                url_reactome_id_stid = 'https://reactome.org/ContentService/data/query/enhanced/' + str(dbid)
                response_enhanced = requests.get(url_reactome_id_stid, headers=headers)
                json_file_enhanced = response_enhanced.text
                stid_return = json.loads(json_file_enhanced)

                for cur_physical_entity in stid_return['physicalEntity']:
                    stid = cur_physical_entity['stId']

                    url_reactome_stid_path = 'https://reactome.org/ContentService/data/pathways/low/entity/' + str(stid)
                    response_pathway = requests.get(url_reactome_stid_path, headers=headers)

                    json_file_pathway = response_pathway.text
                    returned_pathway_list = json.loads(json_file_pathway)

                    for cur_returned_pathway_dict in returned_pathway_list:
                        one_pathway_result_df = pd.DataFrame(columns=pathway_result_df.columns)
                        one_pathway_result_df.at[0, 'KEGG ID'] = kegg_id
                        one_pathway_result_df.at[0, 'compound name'] = stid_return['name']
                        one_pathway_result_df.at[0, 'formula'] = formula
                        one_pathway_result_df.at[0, 'dbId'] = cur_returned_pathway_dict['dbId']
                        one_pathway_result_df.at[0, 'pathway name'] = cur_returned_pathway_dict['displayName']
                        one_pathway_result_df.at[0, 'stId'] = cur_returned_pathway_dict['stId']
                        one_pathway_result_df.at[0, 'isInDisease'] = cur_returned_pathway_dict['isInDisease']
                        one_pathway_result_df.at[0, 'speciesName'] = cur_returned_pathway_dict['speciesName']

                        pathway_result_df = pd.concat([pathway_result_df, one_pathway_result_df])
        else:
            pathway_result_df = pd.DataFrame(
                columns=['KEGG ID', 'compound name', 'formula', 'dbId', 'pathway name', 'stId',
                         'isInDisease', 'speciesName'])
        return pathway_result_df

    def get_reactome_pathway_for_all_compounds(self, kegg_id_list):
        pathway_result_for_all_kegg_ids_df = \
            pd.DataFrame(columns=['KEGG ID', 'compound name', 'formula', 'dbId', 'pathway name', 'stId',
                                  'isInDisease', 'speciesName'])
        for one_kegg_id in kegg_id_list[0:10]:
            print(one_kegg_id)

            pathway_for_one_kegg_id_df = self.get_reactome_pathway_for_one_compound(one_kegg_id)
            if pathway_for_one_kegg_id_df.shape[0] >= 1:
                pathway_result_for_all_kegg_ids_df = pd.concat([pathway_result_for_all_kegg_ids_df,
                                                                pathway_for_one_kegg_id_df])

        if pathway_result_for_all_kegg_ids_df.shape[0] >= 1:
            pathway_result_for_all_kegg_ids_df.reset_index(inplace=True, drop=True)

            out_file_name = 'pathway_result_for_all_kegg_ids.csv'
            out_file_full_name = os.path.join(config.results_dir, out_file_name)
            pathway_result_for_all_kegg_ids_df.to_csv(out_file_full_name)

            print(pathway_result_for_all_kegg_ids_df.head())

        return
    def run(self):
        kegg_id_list = self.get_compounds()
        self.get_reactome_pathway_for_all_compounds(kegg_id_list)
        return


