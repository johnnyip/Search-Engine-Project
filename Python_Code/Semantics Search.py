from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')
import os
import pickle
from sklearn.metrics.pairwise import cosine_similarity as cosine
import numpy as np
from numpy import linalg as LA

os.chdir('C:\\Users\\Lam\\OneDrive - HKUST Connect\\Desktop\\Lecture Note\\CSIT5930\\Project')
f = open('body_content.dat', 'rb')
sentences = pickle.load(f)
# query = 'University Enrollment Method'
query = 'Rubbish and useless film'

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
def cosine_similarity(x, y):
    numerator = abs(np.dot(x, y))
    denominator = LA.norm(x) * LA.norm(y)
    return numerator/denominator

#Encode all sentences
query_embeddings = model.encode(query)


similarity_list = []
for key, value in sentences.items():
    embeddings = model.encode(value)
    similarity = cosine_similarity(embeddings, query_embeddings)
    similarity_list.append([key, similarity])


similarity_list = sorted(similarity_list, key= lambda x:x[1], reverse=True)
print('/','*'*10,'\tSemantic Search Engine\t','*'*10,'/')
print('Query Item:\t', query)
print('Query Result:')
for i in range(5):
    print(similarity_list[i])

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