from bs4 import BeautifulSoup
import requests
import os
import re
from nltk.stem import PorterStemmer
import pickle
import json
from datetime import datetime, timedelta
from nltk.stem import PorterStemmer
import math
import copy
import MongoDB_utilites as MDBU
from pymongo import MongoClient
import sys

class query_retrieval():

    def __init__(self, mongo_host='localhost', mongo_port=27017, stopwords_path='stopwords.txt'):
        f = open(stopwords_path, 'r', encoding='utf-8')
        text = f.read()
        f.close()
        self.stopword_list = text.split('\n')
        self.mongo_client = MongoClient(host=mongo_host, port=mongo_port)
        self.body_inverted_index = dict()
        self.header_inverted_index = dict()
        self.body_df_index = MDBU.retrieve_all_value_from_db(self.mongo_client,DBName='Search_Engine_Data',
                                           CollectionName='Body_DF_Index')
        self.header_df_index = MDBU.retrieve_all_value_from_db(self.mongo_client,DBName='Search_Engine_Data',
                                           CollectionName='Header_DF_Index')
        self.body_tfmax = MDBU.retrieve_all_value_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                                               CollectionName='Body_TFMax_File')
        self.header_tfmax = MDBU.retrieve_all_value_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                                          CollectionName='Header_TFMax_File')
        self.body_doc_length = MDBU.retrieve_all_value_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                                          CollectionName='Body_Doc_Length')
        self.header_doc_length = MDBU.retrieve_all_value_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                                               CollectionName='Header_Doc_Length')
        self.page_rank_index = MDBU.retrieve_all_value_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                                               CollectionName='Page_Rank_Index')
        '''
        word_id = MDBU.retrieve_key_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                           CollectionName='Body_DF_Index')

        for word in word_id:
            temp_dict = dict()
            temp_dict[word] = MDBU.retrieve_value_from_db(self.mongo_client, key=word, DBName='Search_Engine_Data',
                                                         CollectionName='Body_DF_Index')
            self.body_df_index[word] = temp_dict[word]
        print(self.body_df_index)
        self.header_df_index = dict()
        word_id = MDBU.retrieve_key_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                            CollectionName='Header_DF_Index')
        for word in word_id:
            temp_dict = dict()
            temp_dict[word] = MDBU.retrieve_value_from_db(self.mongo_client, key=word, DBName='Search_Engine_Data',
                                                          CollectionName='Header_DF_Index')
            self.header_df_index[word] = temp_dict[word]
        
        self.header_doc_length = dict()
        doc_id = MDBU.retrieve_key_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                           CollectionName='Header_Doc_Length')
        for doc in doc_id:
            temp_dict = dict()
            temp_dict[doc] = MDBU.retrieve_value_from_db(self.mongo_client, key=doc, DBName='Search_Engine_Data',
                                                         CollectionName='Header_Doc_Length')
            self.header_doc_length[doc] = temp_dict[doc]

        self.body_doc_length = dict()
        doc_id = MDBU.retrieve_key_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                           CollectionName='Body_Doc_Length')
        for doc in doc_id:
            temp_dict = dict()
            temp_dict[doc] = MDBU.retrieve_value_from_db(self.mongo_client,key=doc, DBName='Search_Engine_Data',
                                                         CollectionName='Body_Doc_Length')

            self.body_doc_length[doc] = temp_dict[doc]

        self.body_tfmax = dict()
        doc_id = MDBU.retrieve_key_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                           CollectionName='Body_TFMax_File')
        for doc in doc_id:
            temp_dict = dict()
            temp_dict[doc] = MDBU.retrieve_value_from_db(self.mongo_client, key=doc, DBName='Search_Engine_Data',
                                                         CollectionName='Body_TFMax_File')
            self.body_tfmax[doc] = temp_dict[doc]

        self.header_tfmax = dict()
        doc_id = MDBU.retrieve_key_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                           CollectionName='Body_TFMax_File')
        for doc in doc_id:
            temp_dict = dict()
            temp_dict[doc] = MDBU.retrieve_value_from_db(self.mongo_client, key=doc, DBName='Search_Engine_Data',
                                                         CollectionName='Header_TFMax_File')
            self.header_tfmax[doc] = temp_dict[doc]

        self.page_rank_index = dict()
        doc_id = MDBU.retrieve_key_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                           CollectionName='Page_Rank_Index')
        for doc in doc_id:
            temp_dict = dict()
            temp_dict[doc] = MDBU.retrieve_value_from_db(self.mongo_client, key=doc, DBName='Search_Engine_Data',
                                                         CollectionName='Page_Rank_Index')
            self.page_rank_index[doc] = temp_dict[doc]
        '''
        self.page_rank_selection = False

        f = open('word_forward_index.dat','rb')
        self.word_forward_index = pickle.load(f)
        f.close()
        f = open('word_inverted_index.dat', 'rb')
        self.word_inverted_index = pickle.load(f)
        f.close()
        f = open('url_forward_index.dat', 'rb')
        self.url_forward_index = pickle.load(f)
        f.close()
        f = open('url_inverted_index.dat', 'rb')
        self.url_inverted_index = pickle.load(f)
        f.close()

    def stopword_removal(self, inword, stopword_list):

        word = inword.replace(' ', '')
        word = word.lower()
        word = re.sub(pattern='[^0-9a-zA-Z]', repl='', string=word)
        stop_list = stopword_list
        for id, stopword in enumerate(stop_list):
            if word == stopword:
                word = ''
                break
        return word

    def similarity_score_calculation(self, query, type='Body'):
        query_items = query.split()
        document_collection = dict()
        # Removing stopword and stemming the query
        for id, item in enumerate(query_items):
            query_items[id] = self.stopword_removal(inword=item, stopword_list=self.stopword_list)
        ps = PorterStemmer()
        query_items = list(map(ps.stem, query_items))
        for item in query_items:
            if self.word_forward_index.get(item) is None:
                continue
            else:
                item = str(self.word_forward_index[item])
            if type=='Header':
                if self.header_df_index.get(item, 'Null') != 'Null':
                    idf = math.log(float(len(self.header_doc_length)) / float(self.header_df_index[item]))
                    if self.header_inverted_index.get(item, 'Null') != 'Null':
                        for doc in self.header_inverted_index[item].keys():
                            temp = float(len(self.header_inverted_index[item][doc])) * idf / self.header_tfmax[doc]
                            if document_collection.get(doc) is None:
                                document_collection[doc] = temp
                            else:
                                document_collection[doc] = document_collection[doc] + temp
                    else:
                        temp_inverted_file = MDBU.retrieve_value_from_db(self.mongo_client, item,
                                                                         DBName='Search_Engine_Data',
                                                                         CollectionName='Header_Inverted_Index')
                        if len(temp_inverted_file) != 0:
                            for doc in temp_inverted_file[item].keys():
                                temp = len(temp_inverted_file[item][doc]) * idf / self.header_tfmax[doc]
                                if document_collection.get(doc) is None:
                                    document_collection[doc] = temp
                                else:
                                    document_collection[doc] = document_collection[doc] + temp
                            # If size of inverted_index exceeds 1 Gb, the memory of the inverted index would be cleared
                            if (sys.getsizeof(self.header_inverted_index)) / 1024 ** 3 < 1:
                                self.header_inverted_index[item] = temp_inverted_file[item]
                            else:
                                self.header_inverted_index = copy.deepcopy(temp_inverted_file)
            else:
                if self.body_df_index.get(item, 'Null') != 'Null':
                    idf = math.log(float(len(self.body_doc_length)) / float(self.body_df_index[item]))
                    if self.body_inverted_index.get(item, 'Null') != 'Null':
                        for doc in self.body_inverted_index[item].keys():
                            temp = float(len(self.body_inverted_index[item][doc])) * idf / self.body_tfmax[doc]
                            if document_collection.get(doc) is None:
                                document_collection[doc] = temp
                            else:
                                document_collection[doc] = document_collection[doc] + temp
                    else:
                        temp_inverted_file = MDBU.retrieve_value_from_db(self.mongo_client, item,
                                                                       DBName='Search_Engine_Data',
                                                                       CollectionName='Body_Inverted_Index')
                        if len(temp_inverted_file)!=0:
                            for doc in temp_inverted_file[item].keys():
                                temp = len(temp_inverted_file[item][doc]) * idf / self.body_tfmax[doc]
                                if document_collection.get(doc) is None:
                                    document_collection[doc] = temp
                                else: document_collection[doc] = document_collection[doc] + temp
                            # If size of inverted_index exceeds 1 Gb, the memory of the inverted index would be cleared
                            if (sys.getsizeof(self.body_inverted_index))/ 1024 ** 3 < 1:
                                self.body_inverted_index[item] = temp_inverted_file[item]
                            else:
                                self.body_inverted_index = copy.deepcopy(temp_inverted_file)

        query_len = (len(query_items)) ** 0.5
        for key, value in document_collection.items():
            doc_length = self.header_doc_length[key] if type=='header' else self.body_doc_length[key]
            document_collection[key] = value / query_len / doc_length
        temp_test = dict(sorted(document_collection.items(), key=lambda x: x[1], reverse=True))
        return temp_test

    def dict_to_list(self, key, in_list):
        out_list = []
        for item in in_list:
            out_list.append([key, item])
        return out_list

    def phrase_searching(self, query, type1='Body'):
        query_items = query.split()
        document_collection = {}
        full_doc_set = set(list(self.body_doc_length.keys())) if type1=='Body' else set(list(self.header_doc_length.keys()))
        # Removing stopword and stemming the query
        for id, item in enumerate(query_items):
            query_items[id] = self.stopword_removal(inword=item, stopword_list=self.stopword_list)
        ps = PorterStemmer()
        query_items = list(map(ps.stem, query_items))
        tokenize_query_items = list(map(lambda x: str(self.word_forward_index[x]), query_items))
        for item in query_items:
            if self.word_forward_index.get(item) is None:
                break
            else:
                item = str(self.word_forward_index[item])
            temp_inverted_index = dict()
            if type1 == 'Body':
                if self.body_inverted_index.get(item, 'Null') != 'Null':
                    temp_inverted_index = self.body_inverted_index[item]
                elif len(MDBU.retrieve_value_from_db(self.mongo_client, item, CollectionName='Body_Inverted_Index'))!=0:
                    temp_inverted_index = MDBU.retrieve_value_from_db(self.mongo_client, item, CollectionName='Body_Inverted_Index')
                else:
                    temp_inverted_index = dict()
            else:
                if self.header_inverted_index.get(item, 'Null') != 'Null':
                    temp_inverted_index = self.header_inverted_index[item]
                elif len(MDBU.retrieve_value_from_db(self.mongo_client, item, CollectionName='Header_Inverted_Index'))!=0:
                    temp_inverted_index = MDBU.retrieve_value_from_db(self.mongo_client, item, CollectionName='Header_Inverted_Index')
                else:
                    temp_inverted_index = dict()


            if len(temp_inverted_index)>0:
                doc_set = set(list(temp_inverted_index.keys()))
                del_doc_set = full_doc_set - doc_set
                if len(document_collection)!=0:
                    if len(del_doc_set) > 0:
                        for doc in del_doc_set:
                            del document_collection[doc]
                full_doc_set = full_doc_set & doc_set
                for doc in full_doc_set:

                    if document_collection.get(doc, 'Null') == 'Null':
                        temp_list = self.dict_to_list(item, temp_inverted_index[doc])
                        document_collection[doc] = copy.deepcopy(temp_list)

                    else:
                        temp_list = self.dict_to_list(item, temp_inverted_index[doc])
                        temp_list_1 = copy.deepcopy(document_collection[doc])
                        temp_list_1.extend(temp_list)
                        document_collection[doc] = temp_list_1
        del_doc_list = []

        for key in document_collection.keys():
            document_collection[key] = sorted(document_collection[key], key = lambda x : x[1])
            term_list = []
            pos_list = []
            total_count = 0
            for term, pos in document_collection[key]:
                term_list.extend([term])
                pos_list.extend([pos])
            for i in range(len(pos_list)-len(query_items)+1):
                word_count = 0
                if term_list[i] == tokenize_query_items[0]:
                    word_count += 1

                    if len(tokenize_query_items)==1:
                        total_count+=1
                    else:
                        while word_count<len(tokenize_query_items):
                            if term_list[i + word_count] == tokenize_query_items[word_count]:
                                word_count += 1
                            else:
                                break
                            if word_count == len(tokenize_query_items):
                                total_count += 1
            if total_count==0:
                del_doc_list.extend([key])
            else:
                document_collection[key] = total_count
        if len(del_doc_list)>0:
            for doc in del_doc_list:
                del document_collection[doc]
        temp_test = dict(sorted(document_collection.items(), key=lambda x: x[1], reverse=True))
        return temp_test




    def overall_retreival_function(self, query, title_weight=10):
        phrase_query = query.replace('"','<')
        filtered_query = re.sub('<.*?<', '', phrase_query)
        phrase_query = re.findall('<.*?<',phrase_query)
        phrase_query = ' '.join(phrase_query)
        phrase_query = phrase_query.replace('<','')
        filtered_query += ' ' + phrase_query
        body_similarity_score = self.similarity_score_calculation(filtered_query, type='Body')
        header_similarity_score = self.similarity_score_calculation(filtered_query, type='Header')
        return_url_list = copy.deepcopy(body_similarity_score)
        if len(return_url_list)==0:
            return_url_list = copy.deepcopy(header_similarity_score)
            for key, value in return_url_list.items():
                return_url_list[key] = title_weight*value
        else:
            for key, value in header_similarity_score.items():
                if return_url_list.get(key, 'Null') == 'Null':
                    return_url_list[key] = title_weight*value
                else:
                    return_url_list[key] += title_weight*value

        if phrase_query != '':
           body_collection = self.phrase_searching(phrase_query, type1='Body')
           header_collection = self.phrase_searching(phrase_query, type1='Header')
           collection_list = set(list(body_collection.keys())) | set(list(header_collection.keys()))
           del_list = set(list(return_url_list.keys()))
           del_list = list(del_list - collection_list)

           for doc in del_list:
               del return_url_list[doc]

        if self.page_rank_selection == False:
            return_url_list = dict(sorted(return_url_list.items(), key=lambda x: x[1], reverse=True))
        else:
            page_rank_list = copy.deepcopy(self.page_rank_index)
            del_doc_list = set(list(page_rank_list.keys())) - set(list(return_url_list.keys()))
            for doc in del_doc_list:
                del page_rank_list[doc]
            return_url_list = copy.deepcopy(dict(sorted(page_rank_list.items(), key=lambda x: x[1], reverse=True)))
        temp_dict = dict()
        for key in return_url_list.keys():
            temp_key = self.url_inverted_index[int(key)]
            temp_dict[temp_key] = return_url_list[key]
        return_url_list = copy.deepcopy(temp_dict)
        return return_url_list

class page_similarity_search():

    def __init__(self, retreival_engine):
        self.retreival_engine = retreival_engine
        self.forward_index = dict()
        self.mongo_client = MongoClient()

    def page_similarity_search(self, url):
        page_id = str(self.retreival_engine.url_forward_index[url])
        body_forward_index = MDBU.retrieve_value_from_db(self.mongo_client, page_id,
                                                         DBName='Search_Engine_Data',
                                                         CollectionName='Body_Forward_Index')
        head_forward_index = MDBU.retrieve_value_from_db(self.mongo_client, page_id,
                                                         DBName='Search_Engine_Data',
                                                         CollectionName='Header_Forward_Index')




if __name__ == '__main__':
    now = datetime.now()
    os.chdir('C:\\Users\\Lam\\OneDrive - HKUST Connect\\Desktop\\Lecture Note\\CSIT5930\\Project')
    search = query_retrieval()
    now = datetime.now() - now
    print('Initialization Time:',now)
    print('/*********\tOnly_Vector_Space_Model_Algorithm_Apply\t*********/')
    query = 'MOvie "dinosaur" imDB hkust admission ug'
    running_time = datetime.now()
    phrasal_query = str(re.findall('<.*?<', query.replace('"', '<'))[0]).replace('<', '') if len(re.findall('<.*?<', query.replace('"', '<')))>0 else ""
    print('Query:\t\t\t', query, '\n''Phrasal query:\t', phrasal_query,'\n'
          'Search Result:\t',
          search.overall_retreival_function(query))
    running_time = datetime.now() - running_time
    running_min = running_time.total_seconds() // 60
    running_sec = running_time.total_seconds() // 60 * 60
    running_msec = (running_time.total_seconds() - running_time.total_seconds() // 60 * 60) * 1000
    print('Running_time:\t %d min %d sec %.2f ms' % (int(running_min), int(running_sec), running_msec))


    print('/*********\tPage_Rank_Algorithm_Apply\t*********/')
    search.page_rank_selection = True
    query = 'MOvie "dinosaur" imDB hkust admission ug'
    running_time = datetime.now()
    phrasal_query = str(re.findall('<.*?<', query.replace('"', '<'))[0]).replace('<', '') if len(
        re.findall('<.*?<', query.replace('"', '<'))) > 0 else ""
    print('Query:\t\t\t', query, '\n'
                                 'Phrasal query:\t', phrasal_query,
          '\n'
          'Search Result:\t',
          search.overall_retreival_function(query))
    running_time = datetime.now() - running_time
    running_min = running_time.total_seconds() // 60
    running_sec = running_time.total_seconds() // 60 * 60
    running_msec = (running_time.total_seconds() - running_time.total_seconds() // 60 * 60) * 1000
    print('Running_time:\t %d min %d sec %.2f ms' % (int(running_min), int(running_sec), running_msec))
