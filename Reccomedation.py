

import os
import csv
import pandas as pd
import nltk
import string
import pickle
import numpy as np
import random
from stop_words import get_stop_words
from nltk.stem import WordNetLemmatizer
import gensim
from gensim import corpora, models
from sklearn.decomposition import LatentDirichletAllocation
from nltk.stem.porter import PorterStemmer

def jaccard_similarity(query, document):
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return float(len(intersection))/float(len(union))

count=0

path = "/Users/training set/" #modify the path where your training set is present
training=[]
ck=0;
for subdir, dirs, files in os.walk(path):
     
     for file in files:
        
        if file.endswith(".txt"):                        
            count+=1
            
            doc=[]
            
            file_path = subdir + os.path.sep + file
            f= open(file_path, 'r',encoding = "ISO-8859-1")
            content = f.readlines()
            doc=''.join(content)
            doc = doc.replace("\n"," ")
            doc = doc.replace("\'","")
            doc = gensim.utils.simple_preprocess(doc)
            wordnet_lemmatizer = WordNetLemmatizer()
            doc = [wordnet_lemmatizer.lemmatize(word) for word in doc]
            doc = [wordnet_lemmatizer.lemmatize(word,pos='v') for word in doc]
            en_stop = get_stop_words('en')
            letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
            other = ["wa","ha","one","two","id","re","http","com","mr","image","photo","caption","don","sen","pic","co",
                 "source","watch","play","duration","video","momentjs","getty","images","newsletter", "story", "go", "like", "say",
                 "will", "just", "today", "can", "year", "make", "view", "read"]
            doc = [word for word in doc if not word in (en_stop+letters+other)]
            
            
            random.seed(42)
            train_set = random.sample(list(range(0,len(doc))),len(doc))
            train_texts = [doc[i] for i in train_set]
            dummy=[train_texts[i:i+1] for i in range(0,len(train_texts),1)]
            
            dictionary = corpora.Dictionary(dummy)
            
            ldamodels_each_doc={}
            corpus = [dictionary.doc2bow(text) for text in dummy]
            
            num_topics=20
            ldamodels_each_doc = models.ldamodel.LdaModel(corpus,num_topics,id2word=dictionary)
            ldamodels_each_doc.save('/Users/models_for_each_doc/ldamodels_each_doc'+str(count)+'.lda') #modify path to each of your LDA_Models
            lda_topics_string = ldamodels_each_doc.show_topics(num_topics=20,formatted=True)
            
            lda_topics_words = ["".join([c if c.isalpha() else " " for c in topic[1]]).split() for topic in lda_topics_string]
            
            df = pd.DataFrame(lda_topics_words )
            df.to_csv("/Users/topics_of_doc"+str(count)+".csv") #modify path to store your topics mined


count2=0
user_texts=[]        
path = "/Users/user _dataset/" #modify your path to the user_dataset       
for subdir, dirs, files in os.walk(path):
     for file in files:
        count2+=1
        doc=[]
        
        file_path1 = subdir + os.path.sep + file
        f= open(file_path1, 'r',encoding = "ISO-8859-1")
        
        content = f.readlines()
        doc=''.join(content)
        doc = doc.replace("\n"," ")
        doc = doc.replace("\'","")
        doc = gensim.utils.simple_preprocess(doc)
        wordnet_lemmatizer = WordNetLemmatizer()
        doc = [wordnet_lemmatizer.lemmatize(word) for word in doc]
        doc = [wordnet_lemmatizer.lemmatize(word,pos='v') for word in doc]
        en_stop = get_stop_words('en')
        letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        other = ["wa","ha","one","two","id","re","http","com","mr","image","photo","caption","don","sen","pic","co",
             "source","watch","play","duration","video","momentjs","getty","images","newsletter", "story", "go", "like", "say",
             "will", "just", "today", "can", "year", "make", "view", "read"]
        doc = [word for word in doc if not word in (en_stop+letters+other)]
        user_texts.append(doc)
        
     random.seed(42)
     User_train_set = random.sample(list(range(0,len(user_texts[0]))),len(user_texts[0]))
     User_train_texts = [user_texts[0][i] for i in User_train_set]
     User_dummy=[User_train_texts[i:i+1] for i in range(0,len(User_train_texts),1)]
     User_dictionary = corpora.Dictionary(User_dummy)
     
     User_ldamodels={}
     User_corpus = [User_dictionary.doc2bow(text) for text in User_dummy]
     
     num_topics=20
     User_ldamodels = models.ldamodel.LdaModel(User_corpus,num_topics,id2word=User_dictionary)
     User_lda_topics_string = User_ldamodels.show_topics(num_topics=20,formatted=True)
     
     User_lda_topics_words = ["".join([c if c.isalpha() else " " for c in topic[1]]).split() for topic in User_lda_topics_string]
     df = pd.DataFrame(User_lda_topics_words )
     df.to_csv("/Users/User_csvfile/User_topics_of_doc.csv") #modify path to save the user_topics mined
count1=0
doc_topic=[]
Query_topic=[]
name = input("Enter your name ")
print("Hello, %s. Books you read are:-" % name)
print()

fs=pd.read_csv("/Users/usrdata.csv") #modify path to user_data
book_name=fs.values.tolist()
for p in book_name:
    val=p
    str1 = ''.join(val)
    print(os.path.splitext(str1)[0])
    #print(p)
    print()

path= "/Users/csvfile/"  #modify the path where the csv files are stored
print("********* your recommendations  are*********")
print()
for subdir, dirs, files in os.walk(path):
     
     for file in files:
         if file.endswith(".csv"): 
             count1+=1
             topics_each_csv_file=[]
             file_path2 = subdir + os.path.sep + file
             f=pd.read_csv(file_path2)
             topics_each_csv_file=f.values.tolist()
             ft=pd.read_csv("/Users/User_topics_of_doc.csv") #modify the path to user_data_topics
             user_topics=df.values.tolist()
             for i in topics_each_csv_file:
                 for j in i:
                     doc_topic.append(j)
             for i in user_topics:
                 for j in i:
                     Query_topic.append(j)
             sims=(jaccard_similarity(doc_topic,Query_topic))
             sims2=str(round(sims*100,2))
             
             
             if sims2>=str(30):
                 
                 acess=pd.read_csv('/Users/out.csv')  #modify the path which contains the results to print them.
                 file_name=acess.values.tolist()
                 
                 val=file_name[count1-1]
                 str1 = ''.join(val)
                 print(os.path.splitext(str1)[0])
                 
        

