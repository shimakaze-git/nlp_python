from scrayping_request import request_bs_soup
from news_scrayping import get_news_articles


def get_article(path):

    # 記事に対してリクエスト
    soup = request_bs_soup(path)
    text = soup.find('p', class_='yjDirectSLinkTarget').text
    return text


if __name__ == "__main__":
    keyword = '久保建英'
    count = 10
    articles = get_news_articles(keyword, count)

    for path in articles:
        article = get_article(path)
        print(article)
