import configuration
from elasticsearch import Elasticsearch
import json
import pandas as pd

# Making Connection to ElasticSearch for querying the data
ESNN_HOST=configuration.ESNN_HOST
es = Elasticsearch(hosts=[ESNN_HOST],
    http_auth=(configuration.USERNAME, configuration.PASSWORD)
)

# This method is used for searching the machesfashion data and putting into json document
class Process_csv:

    def __init__(self,input_path):
        self.INDEX_NAME=configuration.INDEX_NAME
        self.output_path="output/"
        self.input_path=input_path

    # Converting machesfashion and (ssense, farfetch) json data to csv file 
    def json_to_csv(self):
        maches_json=self.search_index_matchesfashion()
        sensefar_json=self.search_index_ssense_farfetch()
        df1 = pd.read_json(sensefar_json)
        df1.to_csv(self.output_path + "ssense_farftech_matched_products.csv")
        df2 = pd.read_json(maches_json)
        df2.to_csv(self.output_path + "matchesfashion_matched_products.csv")

    # Converting user unique sku data to list of sku
    def fetch_data(self):
        col_names = ['sku']
        list_sku = []
        csvData = pd.read_csv(self.input_path, names=col_names, header=None)
        for i,row in csvData.iterrows():
            list_sku.append(row['sku'])
        return list_sku

    def search_index_matchesfashion(self):

        # This is query body to search across products104 for matching product of machesfashion
        script ={
            "_source": {
                "exclude": [ "*.61fa840764a7e4f3ca859a56","*.6188e422afaf2b4e847b340e","*.6201dd0dd9ff7a61ca7127b4","*.62037d06110b3f66c0238d5c","*.62037c8c110b3f66c0238d5b","*.62037a37110b3f66c0238d5a","*.618a5fcb2324f3ad279b24dc" ]
            },
            "query":{
                "bool":{
                    "must":{
                        "term":{"similar_products.website_results.6189061cb1438e7d97084227.meta.total_results":1}
                    }
                }
            }
        }
        sku_data=self.fetch_data()
        query=es.search(index=self.INDEX_NAME, body=script)
        json_data=[]
        for hit in query["hits"]["hits"]:
            source = hit["_source"]
            source2 = source["similar_products"]["website_results"]["6189061cb1438e7d97084227"]["knn_items"][0]["_source"]

            # Searching the desired sku in sku list so that it will get maapped with only skus present in data
            if source["sku"] in sku_data:
                json_data.append({
                    "SKU":source["sku"],
                    "Net-a-porter Product Name" : source["name"],
                    "Net-a-porter Product Brand" : source["brand"]["sub_brand"] + source["brand"]["name"],
                    "Net-a-porter Product Url" : source["url"],
                    "Net-a-porter Classification Level 1" : source["classification"]["l1"],
                    "Net-a-porter Regular Price" : str(source["price"]["regular_price"]["value"]) + " " + source["price"]["regular_price"]["currency"],
                    "Net-a-porter Offer Price" : str(source["price"]["offer_price"]["value"]) + " " + source["price"]["offer_price"]["currency"],
                    "Net-a-porter Stock" : source["stock"]["available"],
                    "Matchesfashion Product Name" : source2["name"],
                    "Matchesfashion Product Brand" : source2["brand"]["sub_brand"] + source2["brand"]["name"],
                    "Matchesfashion Product Url" : source2["url"],
                    "Matchesfashion Classification Level 1" : source2["classification"]["l1"],
                    "Matchesfashion Regular Price" : str(source2["price"]["regular_price"]["value"]) + " " +  source2["price"]["regular_price"]["currency"],
                    "Matchesfashion Offer Price" : str(source2["price"]["offer_price"]["value"]) + " " + source2["price"]["offer_price"]["currency"],
                    "Matchesfashion Stock" : source2["stock"]["available"]
                })
        return json.dumps(json_data)

    # This method is used for searching the ssense and farfetch data and putting into json document
    def search_index_ssense_farfetch(self):

        # This is query body to search across products104 for matching product of ssense & farfetch
        script ={
        "_source": {
            "exclude": [ "*.61fa840764a7e4f3ca859a56","*.6188e422afaf2b4e847b340e","*.6201dd0dd9ff7a61ca7127b4","*.62037d06110b3f66c0238d5c","*.62037c8c110b3f66c0238d5b","*.6189061cb1438e7d97084227" ]
        },
        "query":{
            "bool": {
            "should": [
                {"term": {"similar_products.website_results.618a5fcb2324f3ad279b24dc.meta.total_results":1}},
                {"term": {"similar_products.website_results.62037a37110b3f66c0238d5a.meta.total_results":1}}
                ]
                }
            }
        }
        json_data=[]
        #This query calls for getting hits after running query body
        sku_data=self.fetch_data()
        query=es.search(index=self.INDEX_NAME, body=script)
        for hit in query["hits"]["hits"]:
            source = hit["_source"]
            source2_ssense = source["similar_products"]["website_results"]["618a5fcb2324f3ad279b24dc"]["knn_items"][0]["_source"]
            source2_farfetch = source["similar_products"]["website_results"]["62037a37110b3f66c0238d5a"]["knn_items"][0]["_source"]

            # Searching the desired sku in sku list so that it will get maapped with only skus present in data
            if source["sku"] in sku_data:
                json_data.append({
                    "SKU":source["sku"],
                    "Net-a-porter Product Name" : source["name"],
                    "Net-a-porter Product Brand" : source["brand"]["sub_brand"] + source["brand"]["name"],
                    "Net-a-porter Regular Price" : str(source["price"]["regular_price"]["value"]) + " " + source["price"]["regular_price"]["currency"],
                    "Net-a-porter Offer Price" : str(source["price"]["offer_price"]["value"]) + " " + source["price"]["offer_price"]["currency"],
                    "Ssense Product Name" : source2_ssense["name"],
                    "Ssense Product Brand" : source2_ssense["brand"]["sub_brand"] + source2_ssense["brand"]["name"],
                    "Ssense Regular Price" : str(source2_ssense["price"]["regular_price"]["value"]) + " " + source2_ssense["price"]["regular_price"]["currency"],
                    "Ssense Offer Price" : str(source2_ssense["price"]["offer_price"]["value"]) + " " + source2_ssense["price"]["offer_price"]["currency"],
                    "Farfetch Product Name" : source2_farfetch["name"],
                    "Farfetch Product Brand" : source2_farfetch["brand"]["sub_brand"] + source2_farfetch["brand"]["name"],
                    "Farfetch Regular Price" : str(source2_farfetch["price"]["regular_price"]["value"]) + " " + source2_farfetch["price"]["regular_price"]["currency"],
                    "Farfetch Offer Price" : str(source2_farfetch["price"]["offer_price"]["value"]) + " " + source2_farfetch["price"]["offer_price"]["currency"]
                })

        return json.dumps(json_data)
