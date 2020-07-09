# worker
from news_scrayping import get_news_articles
from article_scraping import get_article
from ma import split_text_only_noun

from wakati_save import save_wakati_file
from save_word2vec import save_word2vec_model


def worker_wakati_save(keyword, count):

    print('スクレイピング処理')
    articles = get_news_articles(keyword, count)
    list_text = []
    for path in articles:
        article = get_article(path)
        list_text += split_text_only_noun(article)

    print('分かち書き処理')
    # 分かち書き処理
    save_wakati_file(list_text)

    load_path = 'wakati.txt'
    save_model_path = 'save.model'

    # word2vecのモデルの作成
    worker_save_word2vec_model(load_path, save_model_path)


def worker_save_word2vec_model(load_path, save_path):

    print('モデルの作成処理')
    # モデルの作成処理
    save_word2vec_model(load_path, save_path)
