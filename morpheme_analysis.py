#!/usr/bin/env python
"""
Test of MeCab library
"""
import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer


# MeCab による単語への分割関数 (名詞のみ残す)
def split_text_only_noun(text):

    # t = MeCab.Tagger("-d " + DIR_DIC)
    tagger = MeCab.Tagger()

    words = []
    for c in tagger.parse(text).splitlines()[:-1]:
        surface, feature = c.split('\t')
        pos = feature.split(',')[0]
        if pos == '名詞':
            words.append(surface)
    return ' '.join(words)


# TF-IDF の結果からi 番目のドキュメントの特徴的な上位 n 語を取り出す
def extract_feature_words(terms, tfidfs, i, n):
    tfidf_array = tfidfs[i]
    top_n_idx = tfidf_array.argsort()[-n:][::-1]
    words = [terms[idx] for idx in top_n_idx]
    return words


if __name__ == '__main__':
    txts = [
        '私はラーメンが好きです',
        '私は炒飯が好きです',
        '私はプリンが好きです',
        '私は寿司が好きです',
        '私はピサが嫌いです'
    ]

    target_day_nouns = []
    each_nouns = [split_text_only_noun(txt) for txt in txts]
    all_nouns = " ".join(each_nouns)
    target_day_nouns.append(all_nouns)

    # TF-IDF 計算
    tfidf_vectorizer = TfidfVectorizer(
        use_idf=True,
        lowercase=False,
        # max_df=6
    )
    tfidf_matrix = tfidf_vectorizer.fit_transform(target_day_nouns)

    # index 順の単語のリスト
    terms = tfidf_vectorizer.get_feature_names()
    # TF-IDF 行列 (numpy の ndarray 形式)
    tfidfs = tfidf_matrix.toarray()

    i = 0
    for x in extract_feature_words(terms, tfidfs, i, 10):
        print(x)
