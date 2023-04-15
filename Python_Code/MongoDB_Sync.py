import os
import mysql.connector as connector
from mysql.connector import errorcode
from pymongo import MongoClient
from datetime import datetime, timedelta
import math
import copy
import MongoDB_utilites as MDBU
import sqlite3
import pickle

os.chdir('C:\\Users\\Lam\\OneDrive - HKUST Connect\\Desktop\\Lecture Note\\CSIT5930\\Project')
def upload_data_to_mongodb(user='root', password='admin',
                           host='localhost', database='abc',
                           mongo_host='localhost', mongo_port=27017):
    connection = connector.connect(user=user, password=password, host=host, database=database)
    #connection = sqlite3.connect('test.db')
    mongoclient = MongoClient()

    # Update Body Inverted File
    db = mongoclient['Search_Engine_Data']
    collection = db['Body_Inverted_Index']
    collection.drop()

    temp_dict = dict()
    SQL_stmt = 'select StemID, PageID, Position from Alex_StemPos where Type = 2 ' + \
               ' order by stemid, PageID, Position'
    fetch = MDBU.retrieve_from_MySQL(connection, SQL_stmt)
    for f in fetch:
        temp_list = list(map(str, f))
        if len(temp_dict) == 0:
            temp_dict[temp_list[0]] = {temp_list[1]: [f[2]]}
        elif temp_dict.get(temp_list[0], 'Null') == 'Null':
            temp_dict[temp_list[0]] = {temp_list[1]: [f[2]]}
        elif temp_dict[temp_list[0]].get(temp_list[1]) is None:
            temp_dict[temp_list[0]][temp_list[1]] = [f[2]]
        else:
            temp_dict[temp_list[0]][temp_list[1]].extend([f[2]])
    MDBU.Update_Database_from_dict(mongoclient, temp_dict, DBName='Search_Engine_Data',
                                   CollectionName='Body_Inverted_Index')

    # Update Body Forward File
    db = mongoclient['Search_Engine_Data']
    collection = db['Body_Forward_Index']
    collection.drop()

    temp_dict = dict()
    SQL_stmt = 'select PageID, StemID, count(Position) from Alex_StemPos where Type=2'\
               ' group by PageID, StemID order by PageID, StemID'
    fetch = MDBU.retrieve_from_MySQL(connection, SQL_stmt)
    for f in fetch:
        temp_list = list(map(str, f))
        if len(temp_dict) == 0 or temp_dict.get(temp_list[0], 'Null') == 'Null':
            temp_dict[temp_list[0]] = {temp_list[1]: f[2]}
        else:
            temp_dict[temp_list[0]][temp_list[1]] = f[2]

    MDBU.Update_Database_from_dict(mongoclient, temp_dict, DBName='Search_Engine_Data',
                                   CollectionName='Body_Forward_Index')

    # Update Body TF Max File
    db = mongoclient['Search_Engine_Data']
    collection = db['Body_TFMax_File']
    collection.drop()
    SQL_stmt = 'select PageID, max(counter) as TF_Max from ' \
               '(select PageID, StemID, count(*) as counter from Alex_StemPos where type = 2 group by PageID, StemID) as a group by PageID'
    temp_dict = dict()
    for f in MDBU.retrieve_from_MySQL(connection, SQL_stmt):
        temp_list = list(map(str, f))
        temp_dict[temp_list[0]] = f[1]
    MDBU.Update_Database_from_dict(mongoclient, temp_dict, DBName='Search_Engine_Data',
                                   CollectionName='Body_TFMax_File')

    # Update Body DF Index
    db = mongoclient['Search_Engine_Data']
    collection = db['Body_DF_Index']
    collection.drop()
    SQL_stmt = 'select StemID, count(*) from ' \
               '(select StemID, PageID from Alex_StemPos where type = 2 group by StemID, PageID) as a group by StemID'
    temp_dict = dict()
    for f in MDBU.retrieve_from_MySQL(connection, SQL_stmt):
        temp_list = list(map(str, f))
        temp_dict[temp_list[0]] = f[1]
    MDBU.Update_Database_from_dict(mongoclient, temp_dict, DBName='Search_Engine_Data',
                                   CollectionName='Body_DF_Index')
    temp_df = copy.deepcopy(temp_dict)

    # Update Body Doc Length
    db = mongoclient['Search_Engine_Data']
    collection = db['Body_Doc_Length']
    collection.drop()
    cursor = connection.cursor()
    SQL_stmt = 'Drop table if exists tfmax, word_counter'
    cursor.execute(SQL_stmt)

    no_of_pages = len(MDBU.retrieve_key_from_db(client=mongoclient, DBName='Search_Engine_Data',
                                                CollectionName='Body_Forward_Index'))

    SQL_stmt = 'create temporary table tfmax as select PageID, max(counter) as tfmax from ' \
               '(select PageID, StemID, count(*) as counter from Alex_StemPos where type = 2 group by StemID, PageID) as a ' \
               'group by PageID'
    cursor.execute(SQL_stmt)

    SQL_stmt = 'create temporary table word_counter as select PageID, StemID, count(*) as word_count from ' \
               'Alex_StemPos where type = 2 group by PageID, StemID'

    cursor.execute(SQL_stmt)
    SQL_stmt = 'select a.PageID, a.StemID, a.word_count/b.tfmax from word_counter a left join tfmax b on ' \
               'a.PageID = b.PageID'
    temp_dict = dict()
    for f in MDBU.retrieve_from_MySQL(connection, SQL_stmt):
        temp_list = list(map(str, f))
        if temp_dict.get(temp_list[0], 'Null') == 'Null':

            temp_dict[temp_list[0]] = float(f[2]) * math.log2(no_of_pages / temp_df[temp_list[1]])
        else:

            temp_dict[temp_list[0]] += float(f[2]) * math.log2(no_of_pages / temp_df[temp_list[1]])
    MDBU.Update_Database_from_dict(mongoclient, temp_dict, DBName='Search_Engine_Data',
                                   CollectionName='Body_Doc_Length')
    # Update Header Inverted File
    db = mongoclient['Search_Engine_Data']
    collection = db['Header_Inverted_Index']
    collection.drop()

    temp_dict = dict()
    SQL_stmt = 'select StemID, PageID, Position from Alex_StemPos where Type = 1 ' + \
               ' order by stemid, PageID, Position'
    fetch = MDBU.retrieve_from_MySQL(connection, SQL_stmt)
    for f in fetch:
        temp_list = list(map(str, f))
        if len(temp_dict) == 0:
            temp_dict[temp_list[0]] = {temp_list[1]: [f[2]]}
        elif temp_dict.get(temp_list[0], 'Null') == 'Null':
            temp_dict[temp_list[0]] = {temp_list[1]: [f[2]]}
        elif temp_dict[temp_list[0]].get(temp_list[1]) is None:
            temp_dict[temp_list[0]][temp_list[1]] = [f[2]]
        else:
            temp_dict[temp_list[0]][temp_list[1]].extend([f[2]])
    MDBU.Update_Database_from_dict(mongoclient, temp_dict, DBName='Search_Engine_Data',
                                   CollectionName='Header_Inverted_Index')

    # Update Header Forward File
    db = mongoclient['Search_Engine_Data']
    collection = db['Header_Forward_Index']
    collection.drop()

    temp_dict = dict()
    SQL_stmt = 'select PageID, StemID, count(Position) from Alex_StemPos where Type = 1' \
               ' group by PageID, StemID order by PageID, StemID'
    fetch = MDBU.retrieve_from_MySQL(connection, SQL_stmt)
    for f in fetch:
        temp_list = list(map(str, f))
        if len(temp_dict) == 0 or temp_dict.get(temp_list[0], 'Null') == 'Null':
            temp_dict[temp_list[0]] = {temp_list[1]: f[2]}
        else:
            temp_dict[temp_list[0]][temp_list[1]] = f[2]

    MDBU.Update_Database_from_dict(mongoclient, temp_dict, DBName='Search_Engine_Data',
                                   CollectionName='Header_Forward_Index')

    # Update Header TF Max File
    db = mongoclient['Search_Engine_Data']
    collection = db['Header_TFMax_File']
    collection.drop()
    SQL_stmt = 'select PageID, max(counter) as TF_Max from ' \
               '(select PageID, StemID, count(*) as counter from Alex_StemPos where type = 1 group by PageID, StemID) as a group by PageID'
    temp_dict = dict()
    for f in MDBU.retrieve_from_MySQL(connection, SQL_stmt):
        temp_list = list(map(str, f))
        temp_dict[temp_list[0]] = f[1]
    MDBU.Update_Database_from_dict(mongoclient, temp_dict, DBName='Search_Engine_Data',
                                   CollectionName='Header_TFMax_File')

    # Update Header DF Index
    db = mongoclient['Search_Engine_Data']
    collection = db['Header_DF_Index']
    collection.drop()
    SQL_stmt = 'select StemID, count(*) from ' \
               '(select StemID, PageID from Alex_StemPos where type = 1 group by StemID, PageID) as a group by StemID'
    temp_dict = dict()
    for f in MDBU.retrieve_from_MySQL(connection, SQL_stmt):
        temp_list = list(map(str, f))
        temp_dict[temp_list[0]] = f[1]
    MDBU.Update_Database_from_dict(mongoclient, temp_dict, DBName='Search_Engine_Data',
                                   CollectionName='Header_DF_Index')
    temp_df = copy.deepcopy(temp_dict)
    # Update Header Doc Length
    db = mongoclient['Search_Engine_Data']
    collection = db['Header_Doc_Length']
    collection.drop()
    cursor = connection.cursor()
    SQL_stmt = 'Drop table if exists tfmax, word_counter'
    cursor.execute(SQL_stmt)

    no_of_pages = len(MDBU.retrieve_key_from_db(client=mongoclient, DBName='Search_Engine_Data',
                                                CollectionName='Header_Forward_Index'))

    SQL_stmt = 'create temporary table tfmax as select PageID, max(counter) as tfmax from ' \
               '(select PageID, StemID, count(*) as counter from Alex_StemPos where type = 1 group by StemID, PageID) as a ' \
               'group by PageID'
    cursor.execute(SQL_stmt)

    SQL_stmt = 'create temporary table word_counter as select PageID, StemID, count(*) as word_count from ' \
               'Alex_StemPos where type = 1 group by PageID, StemID'

    cursor.execute(SQL_stmt)
    SQL_stmt = 'select a.PageID, a.StemID, a.word_count/b.tfmax from word_counter a left join tfmax b on ' \
               'a.PageID = b.PageID'
    temp_dict = dict()
    for f in MDBU.retrieve_from_MySQL(connection, SQL_stmt):
        temp_list = list(map(str, f))
        if temp_dict.get(temp_list[0], 'Null') == 'Null':
            temp_dict[temp_list[0]] = float(f[2]) * math.log2(no_of_pages / temp_df[temp_list[1]])
        else:
            temp_dict[temp_list[0]] += float(f[2]) * math.log2(no_of_pages / temp_df[temp_list[1]])
    MDBU.Update_Database_from_dict(mongoclient, temp_dict, DBName='Search_Engine_Data',
                                   CollectionName='Header_Doc_Length')


# Perform Page Ranking on the document
def page_rank_index(user='root', password='admin',
                           host='localhost', database='abc',
                           mongo_host='localhost', mongo_port=27017,
                    iternation_no=50, damping_factor=0.8):
    connection = connector.connect(user=user, password=password, host=host, database=database)
    mongoclient = MongoClient(host=mongo_host, port=mongo_port)
    cursor = connection.cursor()
    SQL_stmt = 'select ParentPageId, ChildPageId from Alex_UrlInverted;'
    url_inverted_index = dict()
    for f in MDBU.retrieve_from_MySQL(connection, SQL_stmt):
        templist = list(map(str, f))
        if url_inverted_index.get(templist[0], 'Null')=='Null':
            url_inverted_index[templist[0]] = [templist[1]]
        else:
            url_inverted_index[templist[0]].extend([templist[1]])
    MDBU.Update_Database_from_dict(mongoclient, url_inverted_index, DBName='Search_Engine_Data',
                                   CollectionName='URL_Inverted_Index')

    SQL_stmt = 'select ChildPageId, ParentPageId from Alex_urlforward'
    url_forward_index = dict()
    for f in MDBU.retrieve_from_MySQL(connection, SQL_stmt):
        templist = list(map(str, f))
        if url_forward_index.get(templist[0], 'Null')=='Null':
            url_forward_index[templist[0]] = [f[1]]
        else:
            url_forward_index[templist[0]].extend([f[1]])
    MDBU.Update_Database_from_dict(mongoclient, url_forward_index, DBName='Search_Engine_Data',
                                   CollectionName='URL_Forward_Index')
    page_rank = dict()
    no_of_doc = len(url_forward_index)
    for url in url_forward_index.keys():
        if len(page_rank) == 0:
            page_rank[url] = 1 / no_of_doc
        else:
            page_rank[url] = 1 / no_of_doc
    for i in range(iternation_no):
        normalize_weight = 0
        old_pagerank = copy.deepcopy(page_rank)

        for key, value in page_rank.items():
            prob_from_visit = 0
            for url in url_forward_index[key]:
                prob_to_visit = 1 / len(url_inverted_index[str(url)])
                try:
                    prob_to_visit *= old_pagerank[str(url)]
                except:
                    print(url, old_pagerank)
                    exit()
                prob_from_visit += prob_to_visit

            page_rank[key] = prob_from_visit * damping_factor + (1 - damping_factor)
            normalize_weight += page_rank[key]

        for key in page_rank.keys():
            page_rank[key] = page_rank[key] / normalize_weight
    page_rank = dict(sorted(page_rank.items(), key=lambda x: x[1], reverse=True))
    db = mongoclient['Search_Engine_Data']
    collection = db['Page_Rank_Index']
    collection.drop()
    MDBU.Update_Database_from_dict(mongoclient, page_rank, DBName='Search_Engine_Data',
                                   CollectionName='Page_Rank_Index')
    return page_rank


if __name__ == '__main__':
    now = datetime.now()
    #upload_data_to_mongodb()
    page_rank = page_rank_index()
    os.chdir('C:\\Users\\Lam\\OneDrive - HKUST Connect\\Desktop\\Lecture Note\\CSIT5930\\Project')
    f = open('url_inverted_index.dat','rb')
    url_index = pickle.load(f)
    temp_dict = dict()
    for key in page_rank.keys():
        temp_key = url_index[int(key)]
        print(temp_key)
        temp_dict[temp_key] = page_rank[key]
    temp_dict = dict(sorted(temp_dict.items(), key=lambda x: x[1], reverse=True))
    print(temp_dict)
    now = datetime.now()-now
    print('Running Time: ', now)