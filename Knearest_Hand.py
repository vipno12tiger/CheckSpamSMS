import math
import numpy as np
from random import random

from LastPython import calculate_tfidf, makeData
from LastPython.Document import Document

sigma = 0.005                    # Hệ số
neighbor_number = [3,5,7]             # Số hàng xóm
number_test_datas = [50,40,30]         # Số data test
count = 50                          # số chiều vector

def getDocumentListWithoutVector_and_Corpus(list_doc, list_label):
    Doc_Diction = {}
    for i in range(len(list_doc)):
        flag = list_doc[i]
        pre_label = []
        if Doc_Diction.get(flag) == None:
            pre_label.append(list_label[i])
        else:
            pre_label = Doc_Diction.get(flag)
            if(list_label[i] not in pre_label):
                pre_label.append(list_label[i])
        Doc_Diction.__setitem__(flag, pre_label)

    Document_List = []
    Corpus = []
    for doc in Doc_Diction:
        document = Document(doc, Doc_Diction.get(doc))
        Document_List.append(document)
        Corpus.append(doc)

    return [Corpus, Document_List]


def Doc_to_Vec(tfidf_doc, dictionary):
    vec = []
    for d in dictionary:
        vec.append(tfidf_doc.get(d))
    return vec


def getDocumentListWithVetor(Corpus, Document_List, count):
    tfidf_corpus = calculate_tfidf.calculate_tfidf(Corpus)[0]
    dictionary = calculate_tfidf.getDictionary(tfidf_corpus, count)

    for i in range(len(tfidf_corpus)):
        vec = Doc_to_Vec(tfidf_corpus[i], dictionary)
        Document_List[i].vector = vec
    return Document_List



def computeRank(distance_norm2):
    return math.exp(-1*distance_norm2/sigma)

def getRankWithNeighbor(vec ,DocumentListWithVector):
    for doc in DocumentListWithVector:
        distance_norm2 = 0.0
        doc_vector = doc.vector
        for i in range(len(vec)):
            k = 100
            distance_norm2 = distance_norm2 + (vec[i] - doc_vector[i])*(vec[i] - doc_vector[i])
        doc.rank = computeRank(distance_norm2/k)
    return DocumentListWithVector



def getTestData(DocumentListWithVector, number_test):
    count = 0
    test_data = []
    for i in range(len(DocumentListWithVector)):
        flag = int(180*random()-1)
        test_data.append(DocumentListWithVector[flag])
        DocumentListWithVector.pop(flag)
        count += 1
        if count == number_test:
            break
    return [DocumentListWithVector, test_data]

def key(doc):
    return doc.rank

def test_doc(doc , DocumentListWithVector, number_neighbor):
    test_vec = doc.vector
    RankWithNeighbor = getRankWithNeighbor(test_vec, DocumentListWithVector) # mảng có đầy đủ rank
    rank_list = sorted(RankWithNeighbor, key=key, reverse=True) # mảng sắp xếp rank từ cao xuống thấp

    neighbor_label = []
    number_label = {}
    for i in range(number_neighbor):
        neighbor_label.append(rank_list[i].label)
    list_label = []
    for nb_label in neighbor_label:
        for lb in nb_label:
            list_label.append(lb)

    uniq_label = np.unique(list_label)
    for label in uniq_label:
        count = list_label.count(label)
        number_label.__setitem__(label, count)

    inverse = [(value, key) for key, value in number_label.items()]
    final_label = max(inverse)[1]
    return [getTypeLabel(doc.label), getTypeLabel(final_label)]


def test_corpus(test_data, list_doc_with_vector, number_neighbor):
    count_true = 0
    n = len(test_data)
    for i in range(n):
        doc = test_data[i]
        tes = test_doc(doc, list_doc_with_vector, number_neighbor)
        doc_label = tes[0]
        final_label = tes[1]
        # print(doc_label)
        # print(final_label)
        # print('*'*10)
        if(doc_label == final_label):
            count_true += 1
    return str(100*count_true/n) + '%'


def getTypeLabel(string):
    if 'QC' in string:
        return 'Spam'
    else:
        return 'Non-Spam'


# data = makeData.load_Data("D:\\Giao trinh + Bai tap\\2019-2020\\2019.2\\PythonProject\\LastPython\\Data")
# list_doc = data[0]
# list_label = data[1]
#
# for number_test_data in number_test_datas:
#     print('========', str(number_test_data))
#     for neighbor in neighbor_number:
#         print('*******', str(neighbor))
#         for i in range(10):
#             Corpus = getDocumentListWithoutVector_and_Corpus(list_doc,list_label)[0]
#             DocumentListWithoutVector = getDocumentListWithoutVector_and_Corpus(list_doc, list_label)[1]
#             DocumentListWithVector = getDocumentListWithVetor(Corpus, DocumentListWithoutVector, count)
#
#             a = getTestData(DocumentListWithVector, number_test_data)
#             test_data = a[1]
#             list_doc_with_vector = a[0]
#             print(test_corpus(test_data, list_doc_with_vector, neighbor))
