import os
import re
from datetime import datetime
from nltk.stem import PorterStemmer
import math
import copy
import MongoDB_utilites as MDBU
from pymongo import MongoClient
import sys
from dotenv import load_dotenv
load_dotenv()


class api_query_retrieval():

    def __init__(self, mongo_host=os.environ.get("MONGO_HOST", "localhost"), mongo_port=27017, stopwords_path='data/stopwords.txt'):
        f = open(stopwords_path, 'r', encoding='utf-8')
        text = f.read()
        f.close()
        self.stopword_list = text.split('\n')
        self.mongo_client = MongoClient(host=mongo_host, port=mongo_port)
        self.body_inverted_index = dict()
        self.header_inverted_index = dict()
        self.body_df_index = MDBU.retrieve_all_value_from_db(self.mongo_client, DBName='Search_Engine_Data',
                                                             CollectionName='Body_DF_Index')
        self.header_df_index = MDBU.retrieve_all_value_from_db(self.mongo_client, DBName='Search_Engine_Data',
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
        self.page_rank_selection = False
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
        return_query_match = dict()
        for id, item in enumerate(query_items):
            query_items[id] = self.stopword_removal(inword=item, stopword_list=self.stopword_list)
        ps = PorterStemmer()
        query_items = list(map(ps.stem, query_items))
        for item in query_items:
            if self.word_forward_index.get(item) is None:
                continue
            else:
                item = self.word_forward_index[item]
            if type == 'Header':
                if self.header_df_index.get(item, 'Null') != 'Null':
                    idf = math.log(float(len(self.header_doc_length)) / float(self.header_df_index[item]))
                    if self.header_inverted_index.get(item, 'Null') != 'Null':
                        for doc in self.header_inverted_index[item].keys():
                            temp = float(len(self.header_inverted_index[item][doc])) * idf / self.header_tfmax[doc]
                            if document_collection.get(doc) is None:
                                document_collection[doc] = temp
                            else:
                                document_collection[doc] = document_collection[doc] + temp
                            if return_query_match.get(doc) is None:
                                return_query_match[doc] = [item]
                            else:
                                return_query_match[doc].extend([item])
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
                                if return_query_match.get(doc) is None:
                                    return_query_match[doc] = [item]
                                else:
                                    return_query_match[doc].extend([item])
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
                            if return_query_match.get(doc) is None:
                                return_query_match[doc] = [item]
                            else:
                                return_query_match[doc].extend([item])
                    else:
                        temp_inverted_file = MDBU.retrieve_value_from_db(self.mongo_client, item,
                                                                         DBName='Search_Engine_Data',
                                                                         CollectionName='Body_Inverted_Index')
                        if len(temp_inverted_file) != 0:
                            for doc in temp_inverted_file[item].keys():
                                temp = len(temp_inverted_file[item][doc]) * idf / self.body_tfmax[doc]
                                if document_collection.get(doc) is None:
                                    document_collection[doc] = temp
                                else:
                                    document_collection[doc] = document_collection[doc] + temp
                                if return_query_match.get(doc) is None:
                                    return_query_match[doc] = [item]
                                else:
                                    return_query_match[doc].extend([item])
                            # If size of inverted_index exceeds 1 Gb, the memory of the inverted index would be cleared
                            if (sys.getsizeof(self.body_inverted_index)) / 1024 ** 3 < 1:
                                self.body_inverted_index[item] = temp_inverted_file[item]
                            else:
                                self.body_inverted_index = copy.deepcopy(temp_inverted_file)

        query_len = (len(query_items)) ** 0.5
        for key, value in document_collection.items():
            doc_length = self.header_doc_length[key] if type == 'header' else self.body_doc_length[key]
            document_collection[key] = value / query_len / doc_length
        temp_test = dict(sorted(document_collection.items(), key=lambda x: x[1], reverse=True))
        for key, value in return_query_match.items():
            return_query_match[key] = list(set(value))
        return temp_test, return_query_match

    def dict_to_list(self, key, in_list):
        out_list = []
        for item in in_list:
            out_list.append([key, item])
        return out_list

    def phrase_searching(self, query, type1='Body'):
        query_items = query.split()
        document_collection = {}
        full_doc_set = set(list(self.body_doc_length.keys())) if type1 == 'Body' else set(
            list(self.header_doc_length.keys()))
        # Removing stopword and stemming the query
        for id, item in enumerate(query_items):
            query_items[id] = self.stopword_removal(inword=item, stopword_list=self.stopword_list)
        ps = PorterStemmer()
        query_items = list(map(ps.stem, query_items))
        tokenize_query_items = list(map(lambda x: self.word_forward_index[x], query_items))
        for item in query_items:
            if self.word_forward_index.get(item) is None:
                break
            else:
                item = self.word_forward_index[item]
            temp_inverted_index = dict()
            if type1 == 'Body':
                if self.body_inverted_index.get(item, 'Null') != 'Null':
                    temp_inverted_index = self.body_inverted_index[item]
                elif len(MDBU.retrieve_value_from_db(self.mongo_client, item,
                                                     CollectionName='Body_Inverted_Index')) != 0:
                    temp_inverted_index = MDBU.retrieve_value_from_db(self.mongo_client, item,
                                                                      CollectionName='Body_Inverted_Index')
                else:
                    temp_inverted_index = dict()
            else:
                if self.header_inverted_index.get(item, 'Null') != 'Null':
                    temp_inverted_index = self.header_inverted_index[item]
                elif len(MDBU.retrieve_value_from_db(self.mongo_client, item,
                                                     CollectionName='Header_Inverted_Index')) != 0:
                    temp_inverted_index = MDBU.retrieve_value_from_db(self.mongo_client, item,
                                                                      CollectionName='Header_Inverted_Index')
                else:
                    temp_inverted_index = dict()

            if len(temp_inverted_index) > 0:
                doc_set = set(list(temp_inverted_index.keys()))
                del_doc_set = full_doc_set - doc_set
                if len(document_collection) != 0:
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
            document_collection[key] = sorted(document_collection[key], key=lambda x: x[1])
            term_list = []
            pos_list = []
            total_count = 0
            for term, pos in document_collection[key]:
                term_list.extend([term])
                pos_list.extend([pos])
            for i in range(len(pos_list) - len(query_items) + 1):
                word_count = 0
                if term_list[i] == tokenize_query_items[0]:
                    word_count += 1

                    if len(tokenize_query_items) == 1:
                        total_count += 1
                    else:
                        while word_count < len(tokenize_query_items):
                            if term_list[i + word_count] == tokenize_query_items[word_count]:
                                word_count += 1
                            else:
                                break
                            if word_count == len(tokenize_query_items):
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

    def overall_retreival_function(self, query, title_weight=10):
        phrase_query = query.replace('"', '<')
        filtered_query = re.sub('<.*?<', '', phrase_query)
        phrase_query = re.findall('<.*?<', phrase_query)
        phrase_query = list(map(lambda x: x.replace('<', ''), phrase_query))
        filtered_query += ' ' + ' '.join(phrase_query)
        body_similarity_score, body_query_match_list = self.similarity_score_calculation(filtered_query, type='Body')
        header_similarity_score, header_query_match_list = self.similarity_score_calculation(filtered_query,
                                                                                             type='Header')
        full_query_match_item = dict()
        for key, value in body_query_match_list.items():
            if header_query_match_list.get(key) is not None:
                full_query_match_item[key] = list(set(header_query_match_list[key]) | set(body_query_match_list[key]))
            else:
                full_query_match_item[key] = body_query_match_list[key]
        for key, value in header_query_match_list.items():
            if body_query_match_list.get(key) is None:
                full_query_match_item[key] = header_query_match_list[key]

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

        for item in phrase_query:
            if item != '':
                body_collection = self.phrase_searching(item, type1='Body')
                header_collection = self.phrase_searching(item, type1='Header')
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
            temp_key = self.url_inverted_index[key]
            temp_dict[temp_key] = return_url_list[key]
        return_url_list = copy.deepcopy(temp_dict)
        return_url_items = dict()
        for key in return_url_list.keys():
            return_url_items[key] = self.return_most_frequent_items(self.url_forward_index[key])

        temp_dict = dict()
        for key, value in full_query_match_item.items():
            temp_key = self.url_inverted_index[key]
            temp_dict[temp_key] = list(map(lambda x: self.word_inverted_index[x], full_query_match_item[key]))
            if return_url_list.get(temp_key) is None:
                del temp_dict[temp_key]
        full_query_match_item = copy.deepcopy(temp_dict)

        return_result = list()

        for key, value in return_url_list.items():
            temp_dict = dict()
            temp_key = self.url_forward_index[key]
            temp_dict1 = MDBU.retrieve_value_from_db(self.mongo_client, temp_key,
                                                     DBName='Search_Engine_Data', CollectionName='Display_Layout')
            temp_dict['url'] = key
            temp_dict['Score'] = value
            temp_dict['Matched Key Item'] = full_query_match_item[key]
            temp_dict['Title'] = temp_dict1[temp_key][0]
            temp_dict['Last Modified Date'] = temp_dict1[temp_key][1]
            temp_dict['Size of the Page'] = temp_dict1[temp_key][2]
            temp_dict['Most Frequent Items'] = return_url_items[key]
            temp_list = list()
            if self.url_par_to_chi.get(self.url_forward_index[key]) is not None:
                temp_list = list()
                for item in self.url_par_to_chi[self.url_forward_index[key]]:
                    temp_value = self.url_inverted_index[str(item)]
                    temp_dict_2 = dict()
                    temp_dict_2['url'] = temp_value
                    temp_dict1 = MDBU.retrieve_value_from_db(self.mongo_client, str(item),
                                                             DBName='Search_Engine_Data',
                                                             CollectionName='Display_Layout')
                    temp_dict_2['Title'] = temp_dict1[str(item)][0]
                    temp_list.extend([temp_dict_2])
            temp_dict['Child Link'] = copy.deepcopy(temp_list)
            temp_list = list()
            if self.url_chi_to_par.get(self.url_forward_index[key]) is not None:
                temp_list = list()
                for item in self.url_chi_to_par[self.url_forward_index[key]]:
                    temp_value = self.url_inverted_index[str(item)]
                    temp_dict_2 = dict()
                    temp_dict_2['url'] = temp_value
                    temp_dict1 = MDBU.retrieve_value_from_db(self.mongo_client, str(item),
                                                             DBName='Search_Engine_Data',
                                                             CollectionName='Display_Layout')
                    temp_dict_2['Title'] = temp_dict1[str(item)][0]
                    temp_list.extend([temp_dict_2])
            temp_dict['Parent Link'] = copy.deepcopy(temp_list)
            return_result.extend([temp_dict])
        return return_result, return_url_items

    def page_similarity_search(self, url, original_query):
        self.page_rank_selection = False
        page_id = self.url_forward_index[url]
        body_forward_index = MDBU.retrieve_value_from_db(self.mongo_client, page_id,
                                                         DBName='Search_Engine_Data',
                                                         CollectionName='Body_Forward_Index')
        '''
        header_forward_index = MDBU.retrieve_value_from_db(self.mongo_client, page_id,
                                                           DBName='Search_Engine_Data',
                                                           CollectionName='Header_Forward_Index')
        '''
        temp_list = list(body_forward_index.values())
        temp_list = temp_list[0]
        body_word_index = sorted(temp_list.items(), key=lambda x: x[1], reverse=True)
        full_word_list = dict(body_word_index[:5]).keys()
        '''
        temp_list = list(header_forward_index.values())
        temp_list = temp_list[0]
        header_word_list = list(sorted(temp_list.items(), key=lambda  x:x[1], reverse=True))
        header_word_list = dict(header_word_list[:5]).keys()
        full_word_list = list(set(header_word_list) | set(body_word_index))
        '''

        revised_query = list(map(lambda x: self.word_inverted_index[x], full_word_list))
        revised_query = ' '.join(revised_query)
        revised_query = original_query + ' ' + revised_query
        revised_query = revised_query.replace('"', '')
        return_result, temp_dict = self.overall_retreival_function(revised_query)
        del_key = -9999
        for key, item in enumerate(return_result):
            if item['url'] == url:
                del_key = key
        if del_key != -9999:
            return_result.pop(del_key)
        return_result = return_result
        return_url_items = list()
        for item in return_result:
            temp_dict = dict()
            temp_dict['url'] = item['url']
            temp_dict['item'] = self.return_most_frequent_items(self.url_forward_index[item['url']])
            return_url_items.extend([temp_dict])
        return revised_query, return_result, return_url_items

    def query_vector(self, query):
        running_time = datetime.now()
        search = api_query_retrieval()

        print('/*********\tOnly_Vector_Space_Model_Algorithm_Apply\t*********/')
        # query = 'MOvie "dinosaur" imDB hkust admission ug'
        running_time = datetime.now()
        phrasal_query = str(re.findall('<.*?<', query.replace('"', '<'))[0]).replace('<', '') if len(
            re.findall('<.*?<', query.replace('"', '<'))) > 0 else ""
        search_result, search_frequent_items = search.overall_retreival_function(query)
        print('Query:\t\t\t', query, '\n''Phrasal query:\t', phrasal_query, '\n'
                                                                            'Search Result:\t', search_result)

        running_time = datetime.now() - running_time
        running_min = running_time.total_seconds() // 60
        running_sec = running_time.total_seconds() % 60
        running_msec = running_time.microseconds / 1000
        print('Running_time:\t %d min %d sec %.2f ms' % (int(running_min), int(running_sec), running_msec))
        time = '%d min %d sec %.2f ms' % (int(running_min), int(running_sec), running_msec)

        return {"keyword": query, "result": search_result, "time": time}

    def query_page_rank(self, query):
        print('/*********\tPage_Rank_Algorithm_Apply\t*********/')
        search = api_query_retrieval()
        search.page_rank_selection = True
        running_time = datetime.now()
        phrasal_query = str(re.findall('<.*?<', query.replace('"', '<'))[0]).replace('<', '') if len(
            re.findall('<.*?<', query.replace('"', '<'))) > 0 else ""
        search_result, search_frequent_items = search.overall_retreival_function(query)
        print('Query:\t\t\t', query, '\nPhrasal query:\t', phrasal_query, '\n'
                                                                          'Search Result:\t', search_result)
        running_time = datetime.now() - running_time
        running_min = running_time.total_seconds() // 60
        running_sec = running_time.total_seconds() % 60
        running_msec = running_time.microseconds / 1000
        print('Running_time:\t %d min %d sec %.2f ms' % (int(running_min), int(running_sec), running_msec))
        time = '%d min %d sec %.2f ms' % (int(running_min), int(running_sec), running_msec)

        return {"keyword": query, "result": search_result, "time": time}

    def query_similar(self, url, keyword):
        running_time = datetime.now()
        search = api_query_retrieval()

        print('/*********\tOnly_Vector_Space_Model_Algorithm_Apply\t*********/')
        # query = 'MOvie "dinosaur" imDB hkust admission ug'
        running_time = datetime.now()
        revised_query, return_result, return_url_items = search.page_similarity_search(url, keyword)
        print('Query:\t\t\t', keyword, '\n''Phrasal query:\t', '', '\n'
                                                                            'Search Result:\t', return_result)

        running_time = datetime.now() - running_time
        running_min = running_time.total_seconds() // 60
        running_sec = running_time.total_seconds() % 60
        running_msec = running_time.microseconds / 1000
        print('Running_time:\t %d min %d sec %.2f ms' % (int(running_min), int(running_sec), running_msec))
        time = '%d min %d sec %.2f ms' % (int(running_min), int(running_sec), running_msec)

        return {"keyword": revised_query, "result": return_result, "time": time}
