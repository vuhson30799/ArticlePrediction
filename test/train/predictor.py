import os
import pickle

import gensim  # thư viện NLP
from pyvi import ViTokenizer  # thư viện NLP tiếng Việt
from sklearn.feature_extraction.text import TfidfVectorizer

# word level - we choose max number of words equal to 30000 except all words (100k+ words)
tfidf_vector = TfidfVectorizer(analyzer='word', max_features=30000)
dir_path = os.path.dirname(os.path.realpath(os.getcwd()))
dir_path = os.path.join(dir_path, 'djangoProject', 'test', 'train', 'data')

content_data = pickle.load(open(os.path.join(dir_path, 'X_data.pkl'), 'rb'))
trained_model = pickle.load(open(os.path.join(dir_path, 'finalized_model.sav'), 'rb'))


def predict_specific_content():
    file_path = os.path.join(dir_path, "specific_test.txt")
    content = []
    file = open(file_path, 'r', encoding="utf-8")
    line = file.readlines()
    line = ' '.join(line)
    line = gensim.utils.simple_preprocess(line)
    line = ' '.join(line)
    line = ViTokenizer.tokenize(line)
    content.append(line)

    tfidf_vector.fit(content_data)  # learn vocabulary and idf from training set

    content_data_tfidf = tfidf_vector.transform(content)
    prediction = trained_model.predict(content_data_tfidf)
    return prediction[0]


def predict_articles(articles):
    for article in articles:
        gensim.utils.simple_preprocess(article)
        ViTokenizer.tokenize(article)

    tfidf_vector.fit(content_data)  # learn vocabulary and idf from training set

    content_data_tfidf = tfidf_vector.transform(articles)
    prediction = trained_model.predict(content_data_tfidf)
    return prediction


if __name__ == '__main__':
    print("Type of this article is: " + predict_specific_content())
