import os
from pymongo import MongoClient
import json
import sys
from datetime import datetime, timedelta

def Update_Database_json_update(client, DBName='Search_Engine_Data', CollectionName='Body_Inverted_Index',
                                json_path='body_inverted_index.json'):
    db = client[DBName]
    collection = db[CollectionName]
    collection.drop()
    collection = db[CollectionName]

    # Can replace by retrieving record from MySQL
    f = open(json_path,'r')
    temp_dict = json.load(f)
    f.close()

    for key, value in temp_dict.items():
        collection.insert_one({key: value})

def Update_Database_from_dict(client, input_dict, DBName='Search_Engine_Data', CollectionName='Body_Inverted_Index'):
    db = client[DBName]
    collection = db[CollectionName]
    if len(input_dict) != 0:
        for key, value in input_dict.items():
            temp = {key: value}
            collection.insert_one(temp)

def retrieve_from_MySQL(DB_Connection, SQL_stmt):

    cursor = DB_Connection.cursor()

    cursor.execute(SQL_stmt)
    return cursor.fetchall()




# Retrieve all the keys of documents from MongoDB
def retrieve_key_from_db(client, DBName='Search_Engine_Data', CollectionName='Body_Inverted_Index'):
    db = client[DBName]
    collection = db[CollectionName]
    keys = dict()
    for key in collection.find():
        temp = list(key.keys())
        temp[1]
        keys[temp[1]] = None
    return keys

# Retrieve value of a document from MongoDB
def retrieve_value_from_db(client, key='',DBName='Search_Engine_Data', CollectionName='Body_Inverted_Index'):
    db = client[DBName]
    collection = db[CollectionName]
    projection = {key: 1}
    temp_dict = dict()
    documents = collection.find({key: {'$exists': True}}, projection)
    for document in documents:
        temp_dict[key] = document[key]
        break
    return temp_dict

# Retrieve all documents from MongoDB
def retrieve_all_value_from_db(client, DBName='Search_Engine_Data', CollectionName='Body_Inverted_Index'):
    db = client[DBName]
    collection = db[CollectionName]
    temp_dict = dict()
    #documents = collection.find({key: {'$exists': True}}, projection)
    documents = collection.find()
    temp_dict1 = dict()
    for document in documents:
        temp_dict = document
        del temp_dict['_id']
        temp_key = list(temp_dict.keys())
        temp_dict1[temp_key[0]] = temp_dict[temp_key[0]]
    return temp_dict1

if __name__==('__main__'):
    os.chdir('C:\\Users\\Lam\\OneDrive - HKUST Connect\\Desktop\\Lecture Note\\CSIT5930\\Project')
    running_time = datetime.now()
    DBName = 'Search_Engine_Data'
    CollectionName = 'Body_Inverted_Index'



    client = MongoClient()
    Update_Database_from_dict(client, {'1': 123, '2': 456, '3': 789}, DBName, CollectionName)
    keys = retrieve_key_from_db(client, DBName, CollectionName)
    keys = list(keys)
    print(keys[:10])
    print(sys.getsizeof(keys))

    for key in keys[:10]:
        print(retrieve_value_from_db(client, key=key, DBName=DBName, CollectionName=CollectionName))

    running_time = datetime.now() - running_time
    print(running_time)