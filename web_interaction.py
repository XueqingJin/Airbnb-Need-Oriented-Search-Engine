# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 22:17:28 2019

@author: Yifan Ren
"""
#simply version for quick test
import backend_topN_copy as be_test
import backend_topN as be
import pandas as pd
import webbrowser

def query_url(ranking):
    url_db=pd.read_csv("./urls.csv")
    id_list=[]
    for i in ranking:
        id_list.append(i[0])
    result_df=url_db[url_db["id"].isin(id_list)].set_index("id")
    return result_df

def open_web(i,ranking,result_df):
    url = result_df["listing_url"][ranking[i][0]]
    webbrowser.open(url)

def whether_open(ranking,result_df):
    for i in range(len(ranking)):
        judge=input("Would you like to have a look at the No.{:d} result? [y]/n (or 'exit' to stop): ".format(i+1))
        if judge == "y":
            open_web(i,ranking,result_df)
        elif judge=="n":
            continue
        else:
            if judge!="exit":
                print("Please check your input,and run it again.")
            break

def main():
    print("Start to initialize")
    ranking=be.get_ranking_list()
    result_df=query_url(ranking)
    whether_open(ranking,result_df)




