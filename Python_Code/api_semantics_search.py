# from datetime import datetime
# from sentence_transformers import SentenceTransformer
#
# model = SentenceTransformer('all-MiniLM-L6-v2')
import pickle
import numpy as np
from numpy import linalg as LA
from datetime import datetime, timedelta
import os


class api_semantics_search():

    def __init__(self):
        running_time = datetime.now()

        print("semantics init start")
        f = open('data/body_content.dat', 'rb')
        self.sentences = pickle.load(f)
        print("semantics init done")
        f = open('data/model.dat', 'rb')
        self.model = pickle.load(f)
        f.close()
        self.doc_embedding = dict()
        for key, value in self.sentences.items():
            self.doc_embedding[key] = self.model.encode(value)

        running_time = datetime.now() - running_time
        print('Initialization Time:\t', running_time)

    def cosine_similarity(self, x, y):
        numerator = abs(np.dot(x, y))
        denominator = LA.norm(x) * LA.norm(y)
        return float(numerator / denominator)

    def query_semantics(self, query):
        # query = 'Rubbish and useless film'

        # Encode all sentences
        running_time = datetime.now()

        query_embeddings = self.model.encode(query)

        similarity_list = []
        for key, value in self.doc_embedding.items():
            similarity = self.cosine_similarity(self.doc_embedding[key], query_embeddings)
            similarity_list.append([key, similarity])

        similarity_list = sorted(similarity_list, key=lambda x: x[1], reverse=True)

        running_time = datetime.now() - running_time
        running_min = running_time.total_seconds() // 60
        running_sec = (running_time.total_seconds() % 60) // 1
        running_msec = (running_time.total_seconds() % 1) * 1000
        print('Running_time:\t %d min %d sec %.2f ms' % (int(running_min), int(running_sec), running_msec))
        time = '%d min %d sec %.2f ms' % (int(running_min), int(running_sec), running_msec)

        print('/', '*' * 10, '\tSemantic Search Engine\t', '*' * 10, '/')
        print('Query Item:\t', query)
        print('Query Result:')
        for i in range(5):
            print(similarity_list[i])

        return {"keyword": query, "result": similarity_list[0:5], "time": time}
