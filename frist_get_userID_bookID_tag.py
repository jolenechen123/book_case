#產生1000假的會員紀錄

import random
import pandas as pd
def get_userID_bookID_tag_table():
  

    df = pd.read_csv('jieba4.txt')

    ## 一人與4本書的tags
    b1=random.choice(df["bookno"])
    b1t=df["Jieba"].values[(b1)-1].replace("/",",")  #book1's tag
    b2=random.choice(df["bookno"])
    b2t=df["Jieba"].values[(b2)-1].replace("/",",")  #book2's tag
    b3=random.choice(df["bookno"])
    b3t=df["Jieba"].values[(b3)-1].replace("/",",")  #book3's tag
    b4=random.choice(df["bookno"])
    b4t=df["Jieba"].values[(b4)-1].replace("/",",")  #book4's tag

    m1_tags=[]
    m1_tags.append(b1t)
    m1_tags.append(b2t)
    m1_tags.append(b3t)
    m1_tags.append(b4t)  # member的tags累加

    read_list=[]
    read_list.append(b1)
    read_list.append(b2)
    read_list.append(b3)
    read_list.append(b4)

    
    book_id_list.append(read_list)
    
    tags_list.append(m1_tags)
    
    
    results = {
      "book_id_list": book_id_list,
      "tags_list": tags_list
    }
    return results
#     print(m1_tags)
#     print(read_list)  #看過的書


user_id_list=[]
book_id_list=[]
tags_list=[]

for i in range(0,1000):
    results = get_userID_bookID_tag_table()
    i+=1
    user_id_list.append(i)
    
userID_bookID_tag_df = pd.DataFrame()
userID_bookID_tag_df["user_id"] = user_id_list
userID_bookID_tag_df["book_id_list"] = book_id_list
userID_bookID_tag_df["tags_list"] = tags_list

userID_bookID_tag_df.to_csv("userID_bookID_tag_table.csv", index=False)

