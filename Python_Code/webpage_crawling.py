from bs4 import BeautifulSoup
import requests
import os
import re
import html2text
from nltk.stem import PorterStemmer
import pickle
import json
from datetime import datetime
import copy
import math


class webpage_crawling():
    def __init__(self, body_inverted_index={}, body_forward_index={}, body_df_index={},
                 header_inverted_index={}, header_forward_index={}, header_df_index={}):
        self.html2text = html2text.HTML2Text()
        self.html2text.ignore_links = True
        self.stopword_list = []
        self.url_list = {}
        self.body_inverted_index = body_inverted_index
        self.body_forward_index = body_forward_index
        self.body_df_index = body_df_index
        self.header_inverted_index = header_inverted_index
        self.header_forward_index = header_forward_index
        self.header_df_index = header_df_index
        self.header_doc_length = {}
        self.body_doc_length = {}
        self.url_forward_index = {}
        self.url_inverted_index = {}
        self.page_rank_index = {}
        self.body_content = {}
        self.header_content = {}

    # Search whether a word is within the stopword list
    # If so, replace that word with ''
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

    def doc_length(self, forward_index, inverted_index, df_index):
        new_forward_index = {}
        for doc in forward_index.keys():
            termweight = 0
            for id, item in enumerate(forward_index[doc]):
                for word in forward_index[doc][id].keys():
                    idf = math.log(len(forward_index) / df_index[word], 2)
                    termweight += (inverted_index[word][doc][-1] * idf) ** 2
            termweight = termweight ** 0.5
            new_forward_index[doc] = termweight
        return new_forward_index

    # Page Rank Algorithm with assumption using binary weight.
    def page_rank(self, iternation_no=50, damping_factor=1):
        pagerank = {}
        no_of_doc = len(self.url_forward_index)
        for url in self.url_forward_index.keys():
            if len(pagerank) == 0:
                pagerank[url] = 1 / no_of_doc
            else:
                pagerank[url] = 1 / no_of_doc
        for i in range(iternation_no):
            normalize_weight = 0
            old_pagerank = copy.deepcopy(pagerank)

            for key, value in pagerank.items():
                prob_from_visit = 0
                for url in self.url_forward_index[key]:
                    prob_to_visit = 1 / len(self.url_inverted_index[url])
                    prob_to_visit *= old_pagerank[url]
                    prob_from_visit += prob_to_visit

                pagerank[key] = prob_from_visit * damping_factor + (1 - damping_factor)
                normalize_weight += pagerank[key]

            for key in pagerank.keys():
                pagerank[key] = pagerank[key]
        temp_test = dict(sorted(pagerank.items(), key=lambda x: x[1], reverse=True))
        return temp_test

    # Inverted Index has separated into three parts: updating, deleting and inserting
    # Updating is the combination of deleting and inserting
    # The URL and word will be stored into dict format which is a hash indexing retrieval in Python
    def index_delete(self, url):
        if self.body_forward_index.get(url) is not None:
            list_of_del_word = self.body_forward_index[url]
            del self.body_forward_index[url]
            for word in list_of_del_word:
                del self.body_inverted_index[word][url]
                self.body_df_index[word] -= 1
                if len(self.body_inverted_index[word]) == 0:
                    del self.body_inverted_index[word]
                    del self.body_df_index[word]

    def index_insert(self, url, body_bow, body_stemmed_list, header_bow, header_stemmed_list):
        self.body_forward_index[url] = []
        self.header_forward_index[url] = []
        body_counter = 0
        for word in body_bow:
            counter = 0
            for term in body_stemmed_list:
                if word == term:
                    counter += 1
            body_counter = counter if counter > body_counter else body_counter
        for word in body_bow:
            temp_pos_list = []
            for item, term in enumerate(body_stemmed_list):
                if term == word:
                    temp_pos_list.extend([item + 1])
            self.body_forward_index[url].extend([{word: copy.deepcopy(temp_pos_list)}])
            temp_pos_list.extend([len(temp_pos_list) / body_counter])
            if self.body_inverted_index.get(word) is None:
                self.body_inverted_index[word] = {url: temp_pos_list}
                self.body_df_index[word] = 1
            else:
                self.body_inverted_index[word][url] = temp_pos_list
                self.body_df_index[word] += 1

        header_counter = 0
        for word in header_bow:
            counter = 0
            for term in header_stemmed_list:
                if word == term:
                    counter += 1
            header_counter = counter if counter > header_counter else header_counter
        for word in header_bow:
            temp_pos_list = []
            for item, term in enumerate(header_stemmed_list):
                if term == word:
                    temp_pos_list.extend([item + 1])
            self.header_forward_index[url].extend([{word: copy.deepcopy(temp_pos_list)}])
            temp_pos_list.extend([len(temp_pos_list) / header_counter])
            if self.header_inverted_index.get(word) is None:
                self.header_inverted_index[word] = {url: temp_pos_list}
                self.header_df_index[word] = 1
            else:
                self.header_inverted_index[word][url] = temp_pos_list
                self.header_df_index[word] += 1

    def index_update(self, url, body_bow, body_stemmed_list, header_bow, header_stemmed_list, status):
        if status == 'Update':
            self.index_delete(url)
            self.index_insert(url, body_bow, body_stemmed_list, header_bow, header_stemmed_list)
        elif status == 'Delete':
            self.index_delete(url)
        else:
            self.index_insert(url, body_bow, body_stemmed_list, header_bow, header_stemmed_list)

    def url_update_check(self, urlpath):
        with open(urlpath, 'r', encoding='utf-8') as f:
            Lines = f.readlines()
        f.close()
        updated_url_list = []
        new_url_list = []
        for line in Lines:
            line = line.replace('\n', '')
            temp = line.split(',')
            new_url_list.extend([temp[0]])
            temp[1] = temp[1].lstrip()
            temp[1] = temp[1].replace(' HKT', '')
            last_modified_date = datetime.strptime(temp[1], '%a %b %d %H:%M:%S %Y')
            if self.url_list.get(temp[0]) is None:
                self.url_list[temp[0]] = last_modified_date
                updated_url_list.append([temp[0], 'Insert'])
            elif self.url_list.get(temp[0]) < last_modified_date:
                self.url_list[temp[0]] = temp[1]
                updated_url_list.append([temp[0], 'Update'])
        current_url_set = set(list(self.url_list.keys()))
        del_url_list = list(current_url_set - set(new_url_list))
        for url in del_url_list:
            updated_url_list.append([url, 'Delete'])
        return updated_url_list

    # Parsing HTML page for a specific url
    def page_fetching(self, url, type='body'):
        webfile = requests.get(url)

        if type == 'header':
            html_paser = BeautifulSoup(webfile.content, 'lxml')
            objtag = str(html_paser.find_all('title'))
            web_content = re.sub('<.*?>', repl='', string=objtag)
        else:
            html_paser = BeautifulSoup(webfile.content, 'html.parser')
            objtag = html_paser.decode_contents()
            start = objtag.find('<body>')
            end = objtag.find('</body>')
            objtag = objtag[start:end]
            web_content = self.html2text.handle(objtag)
        web_content = re.sub(pattern="[^0-9a-zA-Z']", repl=' ', string=web_content)
        if type == 'header':
            self.header_content[url] = web_content
        else:
            self.body_content[url] = web_content
        web_content = web_content.split()

        # stopword_removal
        retain_list = []
        for id, word in enumerate(web_content):
            word = self.stopword_removal(inword=word, stopword_list=self.stopword_list)
            if word != '':
                retain_list.extend([word])

        # Porter's Stemming
        ps = PorterStemmer()
        stemmed_list = list(map(ps.stem, retain_list))
        bow = list(set(stemmed_list))
        return bow, stemmed_list

    # Output the index files
    def write_output(self):
        with open('data/Body_Inverted_Index.dat', 'wb') as f:
            pickle.dump(self.body_inverted_index, f)
        f.close()
        del f
        with open('data/Body_Forward_Index.dat', 'wb') as f:
            pickle.dump(self.body_forward_index, f)
        f.close()
        del f
        with open('data/Body_DF_Index.dat', 'wb') as f:
            pickle.dump(self.body_df_index, f)
        f.close()
        del f
        with open('data/Header_Inverted_Index.dat', 'wb') as f:
            pickle.dump(self.header_inverted_index, f)
        f.close()
        del f
        with open('data/Header_Forward_Index.dat', 'wb') as f:
            pickle.dump(self.header_forward_index, f)
        f.close()
        del f
        with open('data/Header_DF_Index.dat', 'wb') as f:
            pickle.dump(self.header_df_index, f)
        f.close()
        del f
        with open('data/stopword_list.dat', 'wb') as f:
            pickle.dump(self.stopword_list, f)
        f.close()
        del f
        with open('data/url_list.dat', 'wb') as f:
            pickle.dump(self.url_list, f)
        f.close()
        del f
        with open('data/header_doc_length.dat', 'wb') as f:
            pickle.dump(self.header_doc_length, f)
        f.close()
        del f
        with open('data/body_doc_length.dat', 'wb') as f:
            pickle.dump(self.body_doc_length, f)
        f.close()
        del f
        with open('data/page_rank_index.dat', 'wb') as f:
            pickle.dump(self.page_rank_index, f)
        f.close()
        del f
        with open('data/body_content.dat', 'wb') as f:
            pickle.dump(self.body_content, f)
        f.close()
        del f
        with open('data/header_content.dat', 'wb') as f:
            pickle.dump(self.header_content, f)
        f.close()
        del f

    # Fetch all webpages' content to inverted index and forward index
    def webpage_content_fetch(self, urllistpath='', stopwordpath=''):
        if stopwordpath != '':
            stopword_path = stopwordpath
            with open(stopword_path, 'r', encoding='utf-8') as f:
                text = f.read()
            f.close()
            self.stopword_list = text.split('\n')

        if urllistpath == '':
            for url in self.body_forward_index.keys():
                body_bow, body_stemmed_list = self.page_fetching(url=url, type='body')
                header_bow, header_stemmed_list = self.page_fetching(url=url, type='header')
                self.index_update(url=url, header_bow=header_bow, header_stemmed_list=header_stemmed_list,
                                  body_bow=body_bow, body_stemmed_list=body_stemmed_list, status='Update')
        else:
            new_url_list = self.url_update_check(urllistpath)
            for url, status in new_url_list:
                body_bow, body_stemmed_list = self.page_fetching(url=url, type='body')
                header_bow, header_stemmed_list = self.page_fetching(url=url, type='header')
                print(url)
                self.index_update(url=url, header_bow=header_bow, header_stemmed_list=header_stemmed_list,
                                  body_bow=body_bow, body_stemmed_list=body_stemmed_list, status='Update')
        self.body_doc_length = self.doc_length(self.body_forward_index, self.body_inverted_index, self.body_df_index)
        self.header_doc_length = self.doc_length(self.header_forward_index, self.header_inverted_index,
                                                 self.header_df_index)
        self.page_rank_index = self.page_rank()
        self.write_output()

    def start(self):
        # os.chdir('data')
        url_path = 'data/url_list_with_date.txt'
        stopword_path = 'data/stopwords.txt'
        f = open('data/url_forward_index.json', 'r')
        url_forward_index = json.load(f)
        f.close()
        del f
        url_inverted_index = {}
        for key, value in url_forward_index.items():
            if len(url_inverted_index) == 0:
                url_inverted_index[value[0]] = []
            else:
                for url in value:
                    if url_inverted_index.get(url, 'Null') == 'Null':
                        templist = [key]
                        url_inverted_index[url] = copy.deepcopy(templist)
                        del templist
                    else:
                        url_inverted_index[url].extend([key])

        fetch = webpage_crawling()

        fetch.url_forward_index = url_forward_index
        fetch.url_inverted_index = url_inverted_index
        fetch.webpage_content_fetch(urllistpath=url_path, stopwordpath=stopword_path)
