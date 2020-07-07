import math
import pandas as pd

from LastPython import makeData


def calculate_tf(word_dict, doc):
    words = doc.split()
    res = {}
    for w in words:
        if w not in res:
            count = 1
            res.__setitem__(w, count)
        else:
            count = res.get(w) + 1
            res.__setitem__(w, count)

    for word in word_dict:
        if word not in res:
            res.__setitem__(word, 0)
    return res


def calculate_idf(word_dict, docs):
    word_count ={}
    res = {}
    for word in word_dict:
        count_word_in_doc = 0
        for doc in docs:
            if word in doc:
                count_word_in_doc += 1
        if count_word_in_doc == 0:
            count_word_in_doc = 1
        idf = math.log(len(docs)/(count_word_in_doc))
        res.__setitem__(word, idf)
        word_count.__setitem__(word,count_word_in_doc)
    # print(word_count)

    return res


def calculate_tfidf(docs):
    word_dict = {}
    for doc in docs:
        words = doc.split()
        for w in words:
            if w not in word_dict:
                word_dict.__setitem__(w, 0)

    tfidf_res = []
    idf_dict = calculate_idf(word_dict, docs)
    for doc in docs:
        res = {}
        tf_dict = calculate_tf(word_dict, doc)
        for word in word_dict:
             tf_idf = tf_dict.get(word) * idf_dict.get(word)
             res.__setitem__(word, tf_idf)
        tfidf_res.append(res)

    final_res = pd.DataFrame(tfidf_res)
    return final_res



data = makeData.load_Data("D:\\Giao trinh + Bai tap\\2019-2020\\2019.2\\PythonProject\\LastPython\\Data")
docs = data[0]
labels = data[1]
# print(labels)
tfidf_dataFrame = calculate_tfidf(docs)
print(tfidf_dataFrame.to_csv("D:\\Giao trinh + Bai tap\\2019-2020\\2019.2\\PythonProject\\LastPython\\DataFrame.csv"))
