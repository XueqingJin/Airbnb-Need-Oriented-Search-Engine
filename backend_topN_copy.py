import pandas as pd
import math
from google.cloud.language import enums
from google.cloud import language_v1
import six
from multiprocessing.dummy import Pool as ThreadPool
import random

def extract_df(date):
    df = pd.read_csv("reviews.csv")
    df['date']=pd.to_datetime(df['date'])
    df_19=df[df['date']> date].reset_index(drop=True)
    df_19["comments"]=df_19["comments"].astype('str')
    return df_19


def extract_keywords(interface_in):
    keywords=interface_in.lower().split(" ")
    keywords_list=set(keywords)
    return keywords_list


def count_idf(word,df):
    doc_num=df.groupby("listing_id").count().shape[0]
    id_set=set()
    for i in range(df.shape[0]):
        try:
            line = df["comments"][i].lower()
        except: continue
        if word in line:
            current_id=df['listing_id'][i]
            if df['listing_id'][i] in id_set:
                df=df[(True^df['listing_id'].isin([current_id]))].copy()
                continue
            else: id_set.add(df['listing_id'][i])
    idf = math.log(doc_num/(len(id_set)+1))
    return {word:idf},id_set

def all_idf(keywords_list,df):
    idf_dict={}
    true_set=set()
    for word in keywords_list:
        idf_dict.update(count_idf(word,df)[0])
        true_set.symmetric_difference_update(count_idf(word,df)[1])
    return idf_dict,true_set

def topn_tfidf(n,df,keywords,idf_dict,true_list):
    grouped=df.groupby("listing_id")["comments"]
    top=[]
    for doc in true_list:
        tf_dict = dict.fromkeys(keywords, 0)
        string=" ".join(grouped.get_group(doc).values).lower().replace("\n","")
        #one word
        one_list=string.split(" ")
        for w in one_list:
            if w in keywords:
                tf_dict[w] =tf_dict[w]+1
            else: continue
        tfidf=0
        for v,k in enumerate(tf_dict):
            tfidf_one=tf_dict[k]*idf_dict[k]
            tfidf+=tfidf_one
        temp_one=(doc,tfidf)
        
        if len(top)<n:
            top.append(temp_one)
            top.sort(key=lambda k: k[1])
        else:
            if temp_one[-1]>top[0][-1]:
                top[0]=temp_one
                top.sort(key=lambda k: k[1])
    return top

def sample_analyze_sentiment(content):

    client = language_v1.LanguageServiceClient()

    # content = 'Your text to analyze, e.g. Hello, world!'

    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': content}

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment
    #print('Score: {}'.format(sentiment.score))
    #print('Magnitude: {}'.format(sentiment.magnitude))
    return sentiment.score

def sa_score(df,tup):
    df_temp=df[df['listing_id']== tup[0]].copy()
    num=len(df_temp)
    total_score=0 
    for line in df_temp["comments"]:
        score=random.random()
        total_score+=score
    avg_score=total_score/num
    new=list(tup)
    new[1]=avg_score*new[1]
    return new

def after_sa_ranking(df,top_n):
    new=[]
    def process2(item):
        new.append(sa_score(df,top_n[item]))
    pool = ThreadPool()
    pool.map(process2, range(len(top_n)))
    pool.close
    pool.join
    new.sort(key=lambda k: k[1],reverse=True)
    return new

def get_ranking_list():
    interface_in = input("What features you perfer? ")
    date=input("From which date? (format like 2019-08-31) ")
    number=int(input("How many candidates? "))
    print("Targeting date range")
    df = extract_df(date)
    keywords=extract_keywords(interface_in)
    print("Calculating IDF")
    idf_dict,true_list=all_idf(keywords,df)
    print("Calculating original ranking based on TFIDF")
    top_n=topn_tfidf(number,df,keywords,idf_dict,true_list)
    print("Calculating adjusted ranking based on Sentiment")
    top_aftersa=after_sa_ranking(df,top_n)
    print("Got it!")
    return top_aftersa
