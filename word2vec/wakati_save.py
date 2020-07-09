from news_scrayping import get_news_articles
from article_scraping import get_article
from ma import split_text_only_noun


# 分かち書きしたデータをファイルに保存
def save_wakati_file(wakati_list, save_path='wakati.txt', add_flag=False):

    # 新規保存か追加保存かの選択
    mode = 'w'
    if add_flag:
        mode = 'a'

    # 分かち書きしたデータをファイルに保存
    with open('./' + save_path, mode=mode, encoding='utf-8') as f:
        f.write(' '.join(wakati_list))


if __name__ == "__main__":
    keyword = '久保建英'
    count = 50
    articles = get_news_articles(keyword, count)

    list_text = []
    for path in articles:
        article = get_article(path)
        list_text += split_text_only_noun(article)

    save_wakati_file(list_text)
