from datetime import datetime
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')
import os
import pickle
from sklearn.metrics.pairwise import cosine_similarity as cosine
import numpy as np
from numpy import linalg as LA


class semantics_search():

    def __init__(self):

        # os.chdir('C:\\Users\\Lam\\OneDrive - HKUST Connect\\Desktop\\Lecture Note\\CSIT5930\\Project')
        f = open('data/body_content.dat', 'rb')
        self.sentences = pickle.load(f)

    '''
    sentences = ['A man is eating food.',
              'A man is eating a piece of bread.',
              'The girl is carrying a baby.',
              'A man is riding a horse.',
              'A woman is playing violin.',
              'Two men pushed carts through the woods.',
              'A man is riding a white horse on an enclosed ground.',
              'A monkey is playing drums.',
              'Someone in a gorilla costume is playing a set of drums.'
              ]
    '''

    def cosine_similarity(self, x, y):
        numerator = abs(np.dot(x, y))
        denominator = LA.norm(x) * LA.norm(y)
        return float(numerator / denominator)

    def query_semantics(self, query):
        query = 'University Enrollment Method'
        # query = 'Rubbish and useless film'

        # Encode all sentences
        running_time = datetime.now()

        query_embeddings = model.encode(query)

        similarity_list = []
        for key, value in self.sentences.items():
            embeddings = model.encode(value)
            similarity = self.cosine_similarity(embeddings, query_embeddings)
            similarity_list.append([key, similarity])

        similarity_list = sorted(similarity_list, key=lambda x: x[1], reverse=True)

        running_time = datetime.now() - running_time
        running_min = running_time.total_seconds() // 60
        running_sec = running_time.total_seconds() // 60 * 60
        running_msec = (running_time.total_seconds() - running_time.total_seconds() // 60 * 60) * 1000
        print('Running_time:\t %d min %d sec %.2f ms' % (int(running_min), int(running_sec), running_msec))
        time = '%d min %d sec %.2f ms' % (int(running_min), int(running_sec), running_msec)

        print('/', '*' * 10, '\tSemantic Search Engine\t', '*' * 10, '/')
        print('Query Item:\t', query)
        print('Query Result:')
        for i in range(5):
            print(similarity_list[i])

        return {"result": similarity_list[0:5], "time": time}

        '''
        #Compute cosine similarity between all pairs
        cos_sim = util.cos_sim(query, embeddings)
        
        print(cos_sim)
        #Add all pairs to a list with their cosine similarity score
        all_sentence_combinations = []
        for i in range(len(cos_sim)-1):
            for j in range(i+1, len(cos_sim)):
                all_sentence_combinations.append([cos_sim[i][j], i, j])
        
        #Sort list by the highest cosine similarity score
        all_sentence_combinations = sorted(all_sentence_combinations, key=lambda x: x[0], reverse=True)
        
        print("Top-5 most similar pairs:")
        for score, i, j in all_sentence_combinations[0:5]:
            print("{} \t {} \t {:.4f}".format(sentences[i], sentences[j], cos_sim[i][j]))
        '''
