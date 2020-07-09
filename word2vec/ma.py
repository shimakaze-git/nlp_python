from news_scrayping import get_news_articles
from article_scraping import get_article

import MeCab


# MeCab による単語への分割関数 (名詞のみ残す)
def split_text_only_noun(text):

    option = '-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd'
    tagger = MeCab.Tagger("-Ochasen " + option)
    tagger.parse('')

    # Execute class analysis
    node = tagger.parseToNode(text)

    words = []
    while node:
        word = node.surface

        class_feature = node.feature.split(',')[0]
        sub_class_feature = node.feature.split(',')[1]

        if class_feature in ['名詞', '動詞', '形容詞', '記号']:
            if sub_class_feature not in ['空白', '*']:
                words.append(word)
        node = node.next
    return words
    # return ' '.join(words)


if __name__ == "__main__":
    keyword = '久保建英'
    count = 10
    articles = get_news_articles(keyword, count)

    list_text = []
    for path in articles:
        article = get_article(path)
        list_text += split_text_only_noun(article)
    print(list_text)
