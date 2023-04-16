from bs4 import BeautifulSoup
import requests
import os
import re
import html2text
from nltk.stem import PorterStemmer
import pickle
import json
from datetime import datetime, timedelta
import webpage_crawling as WebC
from nltk.stem import PorterStemmer
import math
import copy


class api_query_retrieval():

    def __init__(self):
        # os.chdir('data')

        with open('data/Body_Inverted_Index.dat', 'rb') as f:
            body_inverted_index = pickle.load(f)
        f.close()
        del f
        with open('data/Body_Forward_Index.dat', 'rb') as f:
            body_forward_index = pickle.load(f)
        f.close()
        del f
        with open('data/Body_DF_Index.dat', 'rb') as f:
            body_df_index = pickle.load(f)
        f.close()
        del f
        with open('data/Header_Inverted_Index.dat', 'rb') as f:
            header_inverted_index = pickle.load(f)
        f.close()
        del f
        with open('data/Header_Forward_Index.dat', 'rb') as f:
            header_forward_index = pickle.load(f)
        f.close()
        del f
        with open('data/Header_DF_Index.dat', 'rb') as f:
            header_df_index = pickle.load(f)
        f.close()
        del f
        with open('data/stopword_list.dat', 'rb') as f:
            stopword_list = pickle.load(f)
        f.close()
        del f
        with open('data/url_list.dat', 'rb') as f:
            url_list = pickle.load(f)
        f.close()
        del f
        with open('data/header_doc_length.dat', 'rb') as f:
            header_doc_length = pickle.load(f)
        f.close()
        del f
        with open('data/body_doc_length.dat', 'rb') as f:
            body_doc_length = pickle.load(f)
        f.close()
        with open('data/page_rank_index.dat', 'rb') as f:
            page_rank_index = pickle.load(f)
        f.close()
        del f

        self.body_inverted_index = body_inverted_index
        self.body_forward_index = body_forward_index
        self.body_df_index = body_df_index
        self.header_inverted_index = header_inverted_index
        self.header_forward_index = header_forward_index
        self.header_df_index = header_df_index
        self.url_list = url_list
        self.stopword_list = stopword_list
        self.header_doc_length = header_doc_length
        self.body_doc_length = body_doc_length
        self.page_rank_index = page_rank_index
        self.page_rank_selection = False
        self.test = WebC.webpage_crawling()

    def similarity_score_calculation(self, inverted_index, df_index, doc_length, query):
        query_items = query.split()
        document_colletction = {}
        # Removing stopword and stemming the query
        for id, item in enumerate(query_items):
            query_items[id] = self.test.stopword_removal(inword=item, stopword_list=self.stopword_list)
        ps = PorterStemmer()
        query_items = list(map(ps.stem, query_items))
        for item in query_items:
            if df_index.get(item, 'Null') != 'Null':
                idf = math.log(len(inverted_index) / df_index[item])
            if inverted_index.get(item) is not None:
                doc_list = list(inverted_index[item].keys())
                for doc in doc_list:
                    if document_colletction.get(doc) is not None:
                        document_colletction[doc] += inverted_index[item][doc][-1] * idf
                    else:
                        document_colletction[doc] = inverted_index[item][doc][-1] * idf
        query_len = (len(query_items)) ** 0.5
        for key, value in document_colletction.items():
            length_doc = doc_length[key]
            try:
                document_colletction[key] = value / query_len / length_doc
            except:
                print(key, value, length_doc)
                print(doc_length)
        temp_test = dict(sorted(document_colletction.items(), key=lambda x: x[1], reverse=True))
        return temp_test

    def dict_to_list(self, key, in_list):
        out_list = []
        for item in in_list:
            out_list.append([key, item])
        return out_list

    def phrase_searching(self, inverted_index, forward_index, query):
        query_items = query.split()
        document_collection = {}
        full_doc_set = set(list(forward_index.keys()))
        # Removing stopword and stemming the query
        for id, item in enumerate(query_items):
            query_items[id] = self.test.stopword_removal(inword=item, stopword_list=self.stopword_list)
        ps = PorterStemmer()
        query_items = list(map(ps.stem, query_items))
        for item in query_items:
            if inverted_index.get(item) is not None:
                doc_set = set(list(inverted_index[item].keys()))
                del_doc_set = full_doc_set - doc_set
                if len(document_collection) != 0:
                    if len(del_doc_set) > 0:
                        for doc in del_doc_set:
                            del document_collection[doc]
                full_doc_set = full_doc_set & doc_set

                for doc in full_doc_set:

                    if document_collection.get(doc, 'Null') == 'Null':
                        temp_list = self.dict_to_list(item, inverted_index[item][doc][:-1])
                        document_collection[doc] = copy.deepcopy(temp_list)

                    else:
                        temp_list = self.dict_to_list(item, inverted_index[item][doc][:-1])
                        temp_list_1 = copy.deepcopy(document_collection[doc])
                        temp_list_1.extend(temp_list)
                        document_collection[doc] = temp_list_1
        del_doc_list = []
        for key in document_collection.keys():
            document_collection[key] = sorted(document_collection[key], key=lambda x: x[1])
            term_list = []
            pos_list = []
            total_count = 0
            for term, pos in document_collection[key]:
                term_list.extend([term])
                pos_list.extend([pos])
            for i in range(len(pos_list) - len(query_items) + 1):
                word_count = 0
                if term_list[i] == query_items[0]:
                    word_count += 1
                    if len(query_items) == 1:
                        total_count += 1
                    else:
                        while word_count < len(query_items):
                            if term_list[i + word_count] == query_items[word_count]:
                                word_count += 1
                            else:
                                break
                            if word_count == len(query_items):
                                total_count += 1
            if total_count == 0:
                del_doc_list.extend([key])
            else:
                document_collection[key] = total_count
        if len(del_doc_list) > 0:
            for doc in del_doc_list:
                del document_collection[doc]
        temp_test = dict(sorted(document_collection.items(), key=lambda x: x[1], reverse=True))
        return temp_test

    def overall_retreival_function(self, query, title_weight=10):
        phrase_query = query.replace('"', '<')
        filtered_query = re.sub('<.*?<', '', phrase_query)
        phrase_query = re.findall('<.*?<', phrase_query)
        phrase_query = ' '.join(phrase_query)
        phrase_query = phrase_query.replace('<', '')
        body_similarity_score = self.similarity_score_calculation(self.body_inverted_index, self.body_df_index,
                                                                  self.body_doc_length, filtered_query)
        header_similarity_score = self.similarity_score_calculation(self.header_inverted_index, self.header_df_index,
                                                                    self.header_doc_length, filtered_query)
        return_url_list = copy.deepcopy(body_similarity_score)
        if len(return_url_list) == 0:
            return_url_list = copy.deepcopy(header_similarity_score)
            for key, value in return_url_list.items():
                return_url_list[key] = title_weight * value
        else:
            for key, value in header_similarity_score.items():
                if return_url_list.get(key, 'Null') == 'Null':
                    return_url_list[key] = title_weight * value
                else:
                    return_url_list[key] += title_weight * value

        if phrase_query != '':
            body_collection = self.phrase_searching(self.body_inverted_index, self.body_forward_index, phrase_query)
            header_collection = self.phrase_searching(self.header_inverted_index, self.header_forward_index,
                                                      phrase_query)
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
        return return_url_list

    def query_vector(self, query):
        self.page_rank_selection = False

        # search = query_retrieval()
        running_time = datetime.now()

        print('/*********\tOnly_Vector_Space_Model_Algorithm_Apply\t*********/')
        # query = 'MOvie "dinosaur" imDB hkust admission ug'
        matches = re.findall('<.*?<', query.replace('"', '<'))
        phrasal_query = matches[0].replace('<', '') if matches else ""
        result = self.overall_retreival_function(query)
        running_time = datetime.now()
        print('Query:\t\t\t', query, '\n'
                                     'Phrasal query:\t',
              phrasal_query,
              '\n'
              'Search Result:\t',
              result)
        running_time = datetime.now() - running_time
        running_min = running_time.total_seconds() // 60
        running_sec = running_time.total_seconds() // 60 * 60
        running_msec = (running_time.total_seconds() - running_time.total_seconds() // 60 * 60) * 1000
        print('Running_time:\t %d min %d sec %.2f ms' % (int(running_min), int(running_sec), running_msec))
        time = '%d min %d sec %.2f ms' % (int(running_min), int(running_sec), running_msec)

        return {"keyword": query, "result": result, "time": time}

    def query_page_rank(self, query):
        print('/*********\tPage_Rank_Algorithm_Apply\t*********/')
        self.page_rank_selection = True
        # query = 'MOvie "dinosaur" imDB hkust admission ug'
        matches = re.findall('<.*?<', query.replace('"', '<'))
        phrasal_query = matches[0].replace('<', '') if matches else ""
        result = self.overall_retreival_function(query)
        running_time = datetime.now()

        print('Query:\t\t\t', query, '\n'
                                     'Phrasal query:\t',
              phrasal_query,
              '\n'
              'Search Result:\t',
              result)
        running_time = datetime.now() - running_time
        running_min = running_time.total_seconds() // 60
        running_sec = running_time.total_seconds() // 60 * 60
        running_msec = (running_time.total_seconds() - running_time.total_seconds() // 60 * 60) * 1000
        print('Running_time:\t %d min %d sec %.2f ms' % (int(running_min), int(running_sec), running_msec))
        time = '%d min %d sec %.2f ms' % (int(running_min), int(running_sec), running_msec)

        return {"keyword": query, "result": result, "time": time}