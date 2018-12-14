import pandas as pd
import pandas as pd
import numpy as np
import math
import scipy
import sys
import random

# read csv
bookid_jieba_df = pd.read_csv('bktes_jieba_new.txt') #bktes_jieba_new.txt 對書名做jieba的結果
jieba_tag_df = pd.read_csv('text8.txt') # text8.txt = jieba後的自訂義詞庫

standard_tags_list=list(jieba_tag_df["standard_tags"])
standard_tags_list_len=len(standard_tags_list)      # 193個tag

bookTag=[]
for i in range(0,8371):   
    booktxt = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    tag_i = bookid_jieba_df["Jieba"][i]
#     print(tag)
    tag1 = tag_i.split("/")
    print(tag1)
    i = len(tag1)
#     print(i)
    
    for b in range(0,standard_tags_list_len):
        for a in range(0,i):
            if tag1[a]==standard_tags_list[b]:
                booktxt[b] +=1
    bookTag.append(booktxt)
print(bookTag)
book_tag_df = pd.DataFrame()
book_tag_df["book_id"] = book_id
book_tag_df["bookTag"] = bookTag
book_tag_df = book_tag_df.set_index("book_id")

top_book_list = []
for x in range(1,8372):

    sample = np.array(book_tag_df["bookTag"][x])


    cos_list=[]

    for y in range(1,8372):
        ex = np.array(book_tag_df["bookTag"][y])
        tag_dot = np.dot(sample,ex)
        length = math.sqrt(np.sum(sample*sample))*math.sqrt(np.sum(ex*ex))
        cos = float(tag_dot / length)   
        cos_list.append(cos)

    book_tag_df2 = pd.DataFrame()
    book_tag_df2["book_id"] = book_id
    book_tag_df2["cos"] = cos_list
    book_tag_df2 = book_tag_df2.sort_values(by='cos', ascending=False)
    book_tag_df2_TOP7 = book_tag_df2.head(7)
    book_tag_df2_TOP6 = book_tag_df2_TOP7[1:]
    cos_TOP6_book_list = list(book_tag_df2_TOP6["book_id"])
    print(cos_TOP6_book_list)



    top_book_list.append(cos_TOP6_book_list)

    
    
book_topBook_df = pd.DataFrame()
book_topBook_df["book_id"] = book_id
book_topBook_df["top_book_list"] = top_book_list
book_topBook_df.to_csv("cb_table.csv", index=False)