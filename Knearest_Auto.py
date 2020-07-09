from sklearn import neighbors

from LastPython import makeData,Knearest_Hand
from sklearn.model_selection import train_test_split

import numpy as np

count = 50
number_test_data = 50
sigma2 = 0.5

def getVector_Doc_and_Label(DocumentListWithVector):
    docs_vec = []
    labels_vec = []
    for doc in DocumentListWithVector:
        labels = doc.label
        doc_vec = doc.vector
        for label in labels:
            labels_vec.append(label)
            docs_vec.append(doc_vec)

    unique_label = np.unique(labels_vec)
    uniq_lb = 0
    for u_lb in unique_label:
        count = labels_vec.count(u_lb)
        for i in range(count):
            index = labels_vec.index(u_lb)
            labels_vec[index] = uniq_lb
        uniq_lb += 1

    return [docs_vec, labels_vec]


def getType_Of_Label(label_vec):
    for i in range(len(label_vec)):
        lb = label_vec[i]
        flag = 1
        if( 0 <= lb <= 8):
            flag = 0
        label_vec[i] = flag
    return label_vec

def check(label_pred, label_test):
    label_pred = getType_Of_Label(label_pred)
    label_test = getType_Of_Label(label_test)
    count = 0
    for i in range(len(label_pred)):
        if label_pred[i] == label_test[i]:
            count += 1
    return str(100*count/len(label_test)) + '%'


def MyWeight(distances):
    return np.exp(-distances ** 2 / sigma2)



def main():
    data = makeData.load_Data("D:\\Giao trinh + Bai tap\\2019-2020\\2019.2\\PythonProject\\LastPython\\Data")
    list_doc = data[0]
    list_label = data[1]

    Corpus = Knearest_Hand.getDocumentListWithoutVector_and_Corpus(list_doc,list_label)[0]
    DocumentListWithoutVector = Knearest_Hand.getDocumentListWithoutVector_and_Corpus(list_doc, list_label)[1]
    DocumentListWithVector = Knearest_Hand.getDocumentListWithVetor(Corpus, DocumentListWithoutVector, count)

    docs_and_labels_vec = getVector_Doc_and_Label(DocumentListWithVector)
    docs_vec = docs_and_labels_vec[0]
    labels_vec = docs_and_labels_vec[1]

    for i in range(10):
        doc_train, doc_test, label_train, label_test = train_test_split(docs_vec, labels_vec, test_size=number_test_data)

        clf = neighbors.KNeighborsClassifier(n_neighbors = 7, p = 2, weights=MyWeight)
        clf.fit(doc_train, label_train)
        label_pred = clf.predict(doc_test)

        print(check(label_pred,label_test))

# main()