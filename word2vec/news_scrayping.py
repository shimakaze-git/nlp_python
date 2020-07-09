from scrayping_request import request_bs_soup


def get_news_articles(keyword, count):
    url = 'https://news.yahoo.co.jp/search/'
    url += '?p={}&ei=utf-8&fr=news_sw'.format(keyword)

    # 記事リスト
    articles_links = []

    # ページ数
    page = int(count / 10)
    for i in range(1, page + 1):
        path = url + '&b=' + str(i)
        soup = request_bs_soup(path)

        # title部分の取得
        selected_class = soup.select("h2[class='t']")
        articles_links += [s.find('a').get('href') for s in selected_class]

    return articles_links


if __name__ == "__main__":
    keyword = '久保建英'
    count = 100
    articles = get_news_articles(keyword, count)
    print('articles', articles)
