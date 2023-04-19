import os
from pymongo import MongoClient
from datetime import datetime, timedelta
import math
import copy
import MongoDB_utilites as MDBU
import sqlite3
import pickle

os.chdir('C:\\Users\\Lam\\OneDrive - HKUST Connect\\Desktop\\Lecture Note\\CSIT5930\\Project')
def upload_data_to_mongodb(sqlitedb='csit5930',mongo_host='localhost', mongo_port=27017):

    connection = sqlite3.connect(sqlitedb)
    mongoclient = MongoClient()

    # Update Body Inverted File
    db = mongoclient['Search_Engine_Data']
    collection = db['Body_Inverted_Index']
    collection.drop()

    temp_dict = dict()
    SQL_stmt = 'select Stem_ID, Page_ID, Position from stem_token where Type = 2 ' + \
               ' order by Stem_ID, Page_ID, Position'

    fetch = MDBU.retrieve_from_SQLite(connection, SQL_stmt)
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
    SQL_stmt = 'select Page_ID, Stem_ID, count(Position) from stem_token where Type=2'\
               ' group by Page_ID, Stem_ID order by Page_ID, Stem_ID'
    fetch = MDBU.retrieve_from_SQLite(connection, SQL_stmt)
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
    SQL_stmt = 'select Page_ID, max(counter) as TF_Max from ' \
               '(select Page_ID, Stem_ID, count(*) as counter from stem_token where type = 2 group by Page_ID, Stem_ID) as a group by Page_ID'
    temp_dict = dict()
    for f in MDBU.retrieve_from_SQLite(connection, SQL_stmt):
        temp_list = list(map(str, f))
        temp_dict[temp_list[0]] = f[1]
    MDBU.Update_Database_from_dict(mongoclient, temp_dict, DBName='Search_Engine_Data',
                                   CollectionName='Body_TFMax_File')

    # Update Body DF Index
    db = mongoclient['Search_Engine_Data']
    collection = db['Body_DF_Index']
    collection.drop()
    SQL_stmt = 'select Stem_ID, count(*) from ' \
               '(select Stem_ID, Page_ID from stem_token where type = 2 group by Stem_ID, Page_ID) as a group by Stem_ID'
    temp_dict = dict()
    for f in MDBU.retrieve_from_SQLite(connection, SQL_stmt):
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
    SQL_stmt = 'Drop table if exists tfmax;'
    cursor.execute(SQL_stmt)
    SQL_stmt = 'Drop table if exists word_counter;'
    cursor.execute(SQL_stmt)


    no_of_pages = len(MDBU.retrieve_key_from_db(client=mongoclient, DBName='Search_Engine_Data',
                                                CollectionName='Body_Forward_Index'))

    SQL_stmt = 'create temporary table tfmax as select Page_ID, max(counter) as tfmax from ' \
               '(select Page_ID, Stem_ID, count(*) as counter from stem_token where type = 2 group by Stem_ID, Page_ID) as a ' \
               'group by Page_ID'
    cursor.execute(SQL_stmt)

    SQL_stmt = 'create temporary table word_counter as select Page_ID, Stem_ID, count(*) as word_count from ' \
               'stem_token where type = 2 group by Page_ID, Stem_ID'

    cursor.execute(SQL_stmt)
    SQL_stmt = 'select a.Page_ID, a.Stem_ID, a.word_count*1.0/b.tfmax from word_counter a left join tfmax b on ' \
               'a.Page_ID = b.Page_ID'
    temp_dict = dict()
    for f in MDBU.retrieve_from_SQLite(connection, SQL_stmt):
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
    SQL_stmt = 'select Stem_ID, Page_ID, Position from stem_token where Type = 1 ' + \
               ' order by Stem_ID, Page_ID, Position'
    fetch = MDBU.retrieve_from_SQLite(connection, SQL_stmt)
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
    SQL_stmt = 'select Page_ID, Stem_ID, count(Position) from stem_token where Type = 1' \
               ' group by Page_ID, Stem_ID order by Page_ID, Stem_ID'
    fetch = MDBU.retrieve_from_SQLite(connection, SQL_stmt)
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
    SQL_stmt = 'select Page_ID, max(counter) as TF_Max from ' \
               '(select Page_ID, Stem_ID, count(*) as counter from stem_token where type = 1 group by Page_ID, Stem_ID) as a group by Page_ID'
    temp_dict = dict()
    for f in MDBU.retrieve_from_SQLite(connection, SQL_stmt):
        temp_list = list(map(str, f))
        temp_dict[temp_list[0]] = f[1]
    MDBU.Update_Database_from_dict(mongoclient, temp_dict, DBName='Search_Engine_Data',
                                   CollectionName='Header_TFMax_File')

    # Update Header DF Index
    db = mongoclient['Search_Engine_Data']
    collection = db['Header_DF_Index']
    collection.drop()
    SQL_stmt = 'select Stem_ID, count(*) from ' \
               '(select Stem_ID, Page_ID from stem_token where type = 1 group by Stem_ID, Page_ID) as a group by Stem_ID'
    temp_dict = dict()
    for f in MDBU.retrieve_from_SQLite(connection, SQL_stmt):
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
    SQL_stmt = 'Drop table if exists tfmax;'
    cursor.execute(SQL_stmt)
    SQL_stmt = 'Drop table if exists word_counter;'
    cursor.execute(SQL_stmt)

    no_of_pages = len(MDBU.retrieve_key_from_db(client=mongoclient, DBName='Search_Engine_Data',
                                                CollectionName='Header_Forward_Index'))

    SQL_stmt = 'create temporary table tfmax as select Page_ID, max(counter) as tfmax from ' \
               '(select Page_ID, Stem_ID, count(*) as counter from stem_token where type = 1 group by Stem_ID, Page_ID) as a ' \
               'group by Page_ID'
    cursor.execute(SQL_stmt)

    SQL_stmt = 'create temporary table word_counter as select Page_ID, Stem_ID, count(*) as word_count from ' \
               'stem_token where type = 1 group by Page_ID, Stem_ID'

    cursor.execute(SQL_stmt)
    SQL_stmt = 'select a.Page_ID, a.Stem_ID, a.word_count*1.0/b.tfmax from word_counter a left join tfmax b on ' \
               'a.Page_ID = b.Page_ID'
    temp_dict = dict()
    for f in MDBU.retrieve_from_SQLite(connection, SQL_stmt):
        temp_list = list(map(str, f))
        if temp_dict.get(temp_list[0], 'Null') == 'Null':
            temp_dict[temp_list[0]] = float(f[2]) * math.log2(no_of_pages / temp_df[temp_list[1]])
        else:
            temp_dict[temp_list[0]] += float(f[2]) * math.log2(no_of_pages / temp_df[temp_list[1]])
    MDBU.Update_Database_from_dict(mongoclient, temp_dict, DBName='Search_Engine_Data',
                                   CollectionName='Header_Doc_Length')

    # Update the word_inverted_index and word_forward_index
    SQL_stmt = 'select Stem_ID, stem from stem;'
    temp_dict = dict()
    temp_dict_1 = dict()
    for f in MDBU.retrieve_from_SQLite(connection, SQL_stmt):
        temp_list = list(map(str, f))
        if temp_dict.get(temp_list[0]) is None:
            temp_dict[temp_list[0]] = temp_list[1]
            temp_dict_1[temp_list[1]] = temp_list[0]
    MDBU.Update_Database_from_dict(mongoclient, temp_dict, DBName='Search_Engine_Data',
                                   CollectionName='Word_Inverted_Index')
    MDBU.Update_Database_from_dict(mongoclient, temp_dict_1, DBName='Search_Engine_Data',
                                   CollectionName='Word_Forward_Index')

    # Retrieving the raw content for each webpage
    SQL_stmt = 'select url, raw_content from url;'
    temp_dict = dict()
    for f in MDBU.retrieve_from_SQLite(connection, SQL_stmt):
        temp_list = list(map(str, f))
        if temp_dict.get(temp_list[0]) is None:
            temp_dict[temp_list[0]] = temp_list[1]
    MDBU.Update_Database_from_dict(mongoclient, temp_dict, DBName='Search_Engine_Data',
                                   CollectionName='Raw_Page_Content')

    # Retrieving the Page URL, Doc Length, Page Size to MongoDB
    SQL_stmt = 'select page_id, raw_title, last_modified_date, doc_length from url;'
    temp_dict = dict()
    for f in MDBU.retrieve_from_SQLite(connection, SQL_stmt):
        temp_list = list(map(str, f))
        if temp_dict.get(temp_list[0]) is None:
            temp_dict[temp_list[0]] = [temp_list[1], temp_list[2], temp_list[3]]
    MDBU.Update_Database_from_dict(mongoclient, temp_dict, DBName='Search_Engine_Data',
                                   CollectionName='Display_Layout')

# Perform Page Ranking on the document
def page_rank_index(sqlite_db='csit5930', mongo_host='localhost', mongo_port=27017,
                    iternation_no=50, damping_factor=0.8):
    connection = sqlite3.connect(sqlite_db)
    mongoclient = MongoClient(host=mongo_host, port=mongo_port)
    cursor = connection.cursor()

    # Update the url_inverted_index and url_forward_index
    SQL_stmt = 'select page_id, url from url;'
    cursor.execute(SQL_stmt)
    temp_dict = dict()
    temp_dict_1 = dict()
    for f in MDBU.retrieve_from_SQLite(connection, SQL_stmt):
        temp_list = list(map(str, f))
        if temp_dict.get(temp_list[0]) is None:
            temp_dict[temp_list[0]] = temp_list[1]
            temp_dict_1[temp_list[1]] = temp_list[0]
    MDBU.Update_Database_from_dict(mongoclient, temp_dict, DBName='Search_Engine_Data',
                                   CollectionName='ID_To_URL_Index')
    MDBU.Update_Database_from_dict(mongoclient, temp_dict_1, DBName='Search_Engine_Data',
                                   CollectionName='URL_To_ID_Index')


    SQL_stmt = 'select Parent_Page_Id, Child_Page_Id from url_inverted;'
    url_inverted_index = dict()
    for f in MDBU.retrieve_from_SQLite(connection, SQL_stmt):
        templist = list(map(str, f))
        if url_inverted_index.get(templist[0], 'Null')=='Null':
            url_inverted_index[templist[0]] = [templist[1]]
        else:
            url_inverted_index[templist[0]].extend([templist[1]])
    MDBU.Update_Database_from_dict(mongoclient, url_inverted_index, DBName='Search_Engine_Data',
                                   CollectionName='URL_Inverted_Index')

    SQL_stmt = 'select Child_Page_Id, Parent_Page_Id from url_forward'
    url_forward_index = dict()
    for f in MDBU.retrieve_from_SQLite(connection, SQL_stmt):
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
    upload_data_to_mongodb()
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