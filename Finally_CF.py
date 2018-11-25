import pandas as pd
import numpy as np
import math
import scipy
import sys
import random

#選擇資料來源
#read sql
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey
engine = create_engine("mysql+pymysql://root:usbw@localhost:3307/test?charset=utf8")
con = engine.connect()
userID_bookID_tag_df = pd.read_sql_table('userid_bookid_tag_table',con=con)

#  read csv
# userID_bookID_tag_df = pd.read_csv('userID_bookID_tag_table.csv')

user_id=list(userID_bookID_tag_df["user_id"])  # 把欄位裡的user_id轉乘list使用
book_id_list=list(userID_bookID_tag_df["book_id_list"])   # 把欄位裡的book_id_list轉乘list使用
tags_list=list(userID_bookID_tag_df["tags_list"]) # 把欄位裡的tags_list轉乘list使用
jieba_tag_df = pd.read_csv('text8.txt')  # text8.txt內容:討論後決定留下的有效tag
standard_tags_list=list(jieba_tag_df["standard_tags"]) # 把有效tag變成list
standard_tags_list_len=len(standard_tags_list)      # 共193個tag

userTag=[]
for i in range(0,1000):    #range(0,有幾個user)
    # 193個以0為元素的起始矩陣
    usertxt = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    tag_i = userID_bookID_tag_df["tags_list"][i]  # tag_i = tags_list第i個列
    tag1 = tag_i.split(",")  # tag_1 = tag_i分開後的元素
    i = len(tag1) # tag_1的長度
    
    for b in range(0,standard_tags_list_len):
        for a in range(0,i):
            if tag1[a]==standard_tags_list[b]:   # 比對相同的+1
                usertxt[b] +=1
    userTag.append(usertxt)
# userid_userTag_table
user_tag_df = pd.DataFrame()
user_tag_df["user_id"] = user_id
user_tag_df["userTag"] = userTag
user_tag_df = user_tag_df.set_index("user_id")


top_user_list = []
for x in range(1,1001):
    sample = np.array(user_tag_df["userTag"][x])  # 實驗組
    cos_list=[]

    # 將每個實驗組和其餘的做餘弦
    for y in range(1,1001):                     
        ex = np.array(user_tag_df["userTag"][y])
        tag_dot = np.dot(sample,ex)
        length = math.sqrt(np.sum(sample*sample))*math.sqrt(np.sum(ex*ex))
        cos = float(tag_dot / length)   
        cos_list.append(cos)

    user_tag_df2 = pd.DataFrame()
    user_tag_df2["user_id"] = user_id
    user_tag_df2["cos"] = cos_list
    user_tag_df2 = user_tag_df2.sort_values(by='cos', ascending=False)
    user_tag_df2_TOP4 = user_tag_df2.head(4)
    user_tag_df2_TOP3 = user_tag_df2_TOP4[1:]    # 把自己去掉
    cos_TOP3_user_list = list(user_tag_df2_TOP3["user_id"])
    top_user_list.append(cos_TOP3_user_list)

user_topUser_df = pd.DataFrame()
user_topUser_df["user_id"] = user_id
user_topUser_df["top_user_list"] = top_user_list


for p in range(0,1000):
    li = top_user_list[p]  #用戶對照書籍
    for z in li:
        q = z-1
        bookid = userID_bookID_tag_df["book_id_list"][q]

        
user_book_list = []
for p in range(0,1000):
    li = top_user_list[p]
    book_list = []
    for z in li:
        q = z-1
        bookid = userID_bookID_tag_df["book_id_list"][q]
        bookid = bookid.replace("[","")
        bookid = bookid.replace("]","")
        bookid = bookid.split(",")
        
        for a in range(0,4):
            book_list.append(bookid[a])
  
    user_book_list.append(book_list)

finally_user_topUser_df = pd.DataFrame()
finally_user_topUser_df["user_id"] = user_id
finally_user_topUser_df["top_user_list"] = top_user_list
finally_user_topUser_df["user_book_list"] = user_book_list
finally_user_topUser_df.to_csv("userId_topUserList_userBookList_table.csv", index=False)
