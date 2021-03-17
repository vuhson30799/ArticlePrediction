from newspaper import Article

from test.train.predictor import predict_articles

TEXT_CONSTANT = "Something went wrong with this url..."


class Result:
    def __init__(self, *args):
        self.url = args[0]
        self.topic = args[1]


def get_article_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
    except:
        return TEXT_CONSTANT + url
    return article.text


def predict_from_urls(urls):
    url_list = urls.splitlines()
    contents = []
    for url in url_list:
        content = get_article_content(url)
        contents.append(content)

    predictions = predict_articles(contents)

    result_list = []
    url_list.reverse()
    for prediction in predictions:
        result = Result(url_list.pop(), prediction)
        result_list.append(result)

    return result_list
