import os
import pickle

import gensim  # thư viện NLP
from pyvi import ViTokenizer  # thư viện NLP tiếng Việt
from sklearn import metrics, naive_bayes
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm

# word level - we choose max number of words equal to 30000 except all words (100k+ words)
tfidf_vector = TfidfVectorizer(analyzer='word', max_features=30000)
dir_path = os.path.dirname(os.path.realpath(os.getcwd()))
dir_path = os.path.join(dir_path, 'train', 'data')


def get_data(folder_path):
    content = []
    label = []
    dirs = os.listdir(folder_path)
    for path in tqdm(dirs):
        file_paths = os.listdir(os.path.join(folder_path, path))
        for file_path in tqdm(file_paths):
            with open(os.path.join(folder_path, path, file_path), 'r', encoding="utf-16") as f:
                lines = f.readlines()
                lines = ' '.join(lines)
                lines = gensim.utils.simple_preprocess(lines)
                lines = ' '.join(lines)
                lines = ViTokenizer.tokenize(lines)

                content.append(lines)
                label.append(path)

    return content, label


def test_train_model(classifier, content_test_tfidf, label_test):
    print("Start testing model...")
    test_predictions = classifier.predict(content_test_tfidf)
    print("Test accuracy: ", metrics.accuracy_score(test_predictions, label_test))


def train_model():
    classifier = naive_bayes.MultinomialNB()

    train_path = os.path.join(dir_path, 'train_data')

    content_data, label_data = get_data(train_path)
    pickle.dump(content_data, open(os.path.join(dir_path, 'X_data.pkl'), 'wb'))
    pickle.dump(label_data, open(os.path.join(dir_path, 'y_data.pkl'), 'wb'))

    test_path = os.path.join(dir_path, 'test_data')

    content_test, label_test = get_data(test_path)
    pickle.dump(content_test, open(os.path.join(dir_path, 'X_test.pkl'), 'wb'))
    pickle.dump(label_test, open(os.path.join(dir_path, 'y_test.pkl'), 'wb'))

    content_data = pickle.load(open(os.path.join(dir_path, 'X_data.pkl'), 'rb'))
    label_data = pickle.load(open(os.path.join(dir_path, 'y_data.pkl'), 'rb'))

    content_test = pickle.load(open(os.path.join(dir_path, 'X_test.pkl'), 'rb'))
    label_test = pickle.load(open(os.path.join(dir_path, 'y_test.pkl'), 'rb'))

    tfidf_vector.fit(content_data)  # learn vocabulary and idf from training set
    content_data_tfidf = tfidf_vector.transform(content_data)
    content_test_tfidf = tfidf_vector.transform(content_test)

    classifier = classifier.fit(content_data_tfidf, label_data)
    print("Training completely!!!")

    test_train_model(classifier, content_test_tfidf, label_test)
    return classifier


def save_model(model):
    file_name = os.path.join(dir_path, "finalized_model.sav")
    pickle.dump(model, open(file_name, 'wb'))


if __name__ == '__main__':
    trained_model = train_model()
    save_model(trained_model)
