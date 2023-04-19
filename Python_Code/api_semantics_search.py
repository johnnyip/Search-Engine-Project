from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
# model = SentenceTransformer('all-MiniLM-L6-v2')
import pickle
import numpy as np
from numpy import linalg as LA
from datetime import datetime
import os
import MongoDB_utilites as MDBU
import copy


class api_semantics_search():

    def __init__(self):


        print("semantics init start")
        self.mongo_client = MongoClient()
        self.sentences = MDBU.retrieve_all_value_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                                           CollectionName='Raw_Page_Content')
        print("semantics init done")
        f = open('data/model.dat', 'rb')
        self.model = pickle.load(f)
        f.close()
        self.doc_embedding = dict()
        for key, value in self.sentences.items():
            self.doc_embedding[key] = self.model.encode(value)

        self.word_forward_index = MDBU.retrieve_all_value_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                                                  CollectionName='Word_Forward_Index')
        self.word_inverted_index = MDBU.retrieve_all_value_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                                                   CollectionName='Word_Inverted_Index')
        self.url_forward_index = MDBU.retrieve_all_value_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                                                 CollectionName='URL_To_ID_Index')
        self.url_inverted_index = MDBU.retrieve_all_value_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                                                  CollectionName='ID_To_URL_Index')
        self.url_par_to_chi = MDBU.retrieve_all_value_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                                              CollectionName='URL_Inverted_Index')
        self.url_chi_to_par = MDBU.retrieve_all_value_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                                              CollectionName='URL_Forward_Index')

    def cosine_similarity(self, x, y):
        numerator = np.dot(x, y)
        denominator = LA.norm(x) * LA.norm(y)
        return float(numerator / denominator)

    def return_most_frequent_items(self, page_id):
        temp_dict = MDBU.retrieve_value_from_db(self.mongo_client, page_id, CollectionName='Body_Forward_Index')
        temp_dict = temp_dict[page_id]
        temp_list = sorted(temp_dict.items(), key=lambda x: x[1], reverse=True)
        temp_list = temp_list[:5]
        temp_list1 = list()
        for item in temp_list:
            temp_dict = dict()
            temp_key = self.word_inverted_index[item[0]]
            temp_dict['Item'] = temp_key
            temp_dict['Frequency'] = item[1]
            temp_list1.extend([copy.deepcopy(temp_dict)])
        return temp_list1

    def query_semantics(self, query):
        running_time = datetime.now()

        query_embeddings = self.model.encode(query)

        similarity_list = []
        for key, value in self.doc_embedding.items():
            similarity = self.cosine_similarity(self.doc_embedding[key], query_embeddings)
            similarity_list.append([key, similarity])

        similarity_list = sorted(similarity_list, key=lambda x: x[1], reverse=True)
        similarity_list = similarity_list[:5]

        return_result = list()

        for item in similarity_list:
            temp_dict = dict()
            temp_dict['url'] = item[0]
            temp_dict['Score'] = item[1]


            temp_key = self.url_forward_index[item[0]]
            temp_dict1 = MDBU.retrieve_value_from_db(self.mongo_client, temp_key,
                                                     DBName='Search_Engine_Data', CollectionName='Display_Layout')
            temp_dict['Title'] = temp_dict1[temp_key][0]
            temp_dict['Last Modified Date'] = temp_dict1[temp_key][1]
            temp_dict['Size of the Page'] = temp_dict1[temp_key][2]
            temp_dict['Most Frequent Items'] = self.return_most_frequent_items(self.url_forward_index[item[0]])

            temp_list = list()
            if self.url_par_to_chi.get(self.url_forward_index[item[0]]) is not None:
                temp_list = list()
                for item1 in self.url_par_to_chi[self.url_forward_index[item[0]]]:
                    temp_value = self.url_inverted_index[str(item1)]
                    temp_dict_2 = dict()
                    temp_dict_2['url'] = temp_value
                    temp_dict1 = MDBU.retrieve_value_from_db(self.mongo_client, str(item1),
                                                             DBName='Search_Engine_Data',
                                                             CollectionName='Display_Layout')
                    temp_dict_2['Title'] = temp_dict1[str(item1)][0]
                    temp_list.extend([temp_dict_2])
            temp_dict['Parent Link'] = copy.deepcopy(temp_list)
            temp_list = list()
            if self.url_chi_to_par.get(self.url_forward_index[item[0]]) is not None:
                temp_list = list()
                for item1 in self.url_chi_to_par[self.url_forward_index[item[0]]]:
                    temp_value = self.url_inverted_index[str(item1)]
                    temp_dict_2 = dict()
                    temp_dict_2['url'] = temp_value
                    temp_dict1 = MDBU.retrieve_value_from_db(self.mongo_client, str(item1),
                                                             DBName='Search_Engine_Data',
                                                             CollectionName='Display_Layout')
                    temp_dict_2['Title'] = temp_dict1[str(item1)][0]
                    temp_list.extend([temp_dict_2])
            temp_dict['Child Link'] = copy.deepcopy(temp_list)
            return_result.extend([temp_dict])

        running_time = datetime.now() - running_time
        running_min = running_time.total_seconds() // 60
        running_sec = (running_time.total_seconds() % 60) // 1
        running_msec = (running_time.total_seconds() % 1) * 1000
        print('Running_time:\t %d min %d sec %.2f ms' % (int(running_min), int(running_sec), running_msec))
        time = '%d min %d sec %.2f ms' % (int(running_min), int(running_sec), running_msec)

        print('/', '*' * 10, '\tSemantic Search Engine\t', '*' * 10, '/')
        print('Query Item:\t', query)
        print('Query Result:')
        for item in return_result:
            print(item)

        return {"keyword": query, "result": return_result, "time": time}
