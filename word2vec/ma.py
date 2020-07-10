from news_scrayping import get_news_articles
from article_scraping import get_article
from scrayping_request import request_bs_soup

import MeCab
import re


# ストップワード
def create_stop_word():
    target_url = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
    soup = request_bs_soup(target_url)
    stop_word = str(soup).split()

    return stop_word


# 不必要な文字列を削除する.
def delete_word(text):
    # 記号の削除
    text = re.sub("[!-/:-@[-`{-~]", "", text)
    text = re.sub("[:・。、『』*－?！？]", "", text)

    l_text = [
        '（[^（|^）]*）',
        '【[^【|^】]*】',
        '＜[^＜|^＞]*＞',
        '［[^［|^］]*］',
        '「[^「|^」]*」',
        '｛[^｛|^｝]*｝',
        '〔[^〔|^〕]*〕',
        '〈[^〈|^〉]*〉'
    ]
    for l_ in l_text:
        text = re.sub(l_, "", text)

    # 空白・改行の削除
    text = re.sub(u'\n\n', '\n', text)
    text = re.sub(u'\r', '', text)

    return text


# MeCab による単語への分割関数 (名詞のみ残す)
def split_text_only_noun(text):

    option = '-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd'
    tagger = MeCab.Tagger("-Ochasen " + option)
    tagger.parse('')

    # Execute class analysis
    node = tagger.parseToNode(text)

    stop_word = create_stop_word()

    words = []
    while node:
        word = node.surface

        class_feature = node.feature.split(',')[0]
        sub_class_feature = node.feature.split(',')[1]

        if class_feature == '名詞':
            if (
                sub_class_feature not in ['空白', '*']
            ) and not (word in stop_word):
                words.append(word)

        if class_feature in ['動詞', '形容詞', '形容動詞', '記号']:
            word = node.feature.split(',')[6]
            if (
                sub_class_feature not in ['空白', '*']
            ) and not (word in stop_word):
                words.append(word)
        node = node.next
    return words


if __name__ == "__main__":
    keyword = '久保建英'
    count = 10
    articles = get_news_articles(keyword, count)

    list_text = []
    for path in articles:
        article = get_article(path)
        article = delete_word(article)
        list_text += split_text_only_noun(article)
