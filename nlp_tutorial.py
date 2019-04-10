#!/usr/bin/env python

import numpy as np
import MeCab

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


# MeCab による単語への分割関数 (名詞のみ残す)
def split_text_only_noun(text):
    tagger = MeCab.Tagger()
    words = []
    for c in tagger.parse(text).splitlines()[:-1]:
        surface, feature = c.split('\t')
        pos = feature.split(',')[0]
        if pos == '名詞':
            words.append(surface)
    return ' '.join(words)


# コサイン類似度
def cos_sim(v1, v2):
    v1_v2 = np.dot(v1, v2)
    v1_v2_norm = (np.linalg.norm(v1) * np.linalg.norm(v2))
    return v1_v2 / v1_v2_norm


python_1 = '''
Python は強力で、学びやすいプログラミング言語です。
効率的な高レベルデータ構造と、シンプルで効果的なオブジェクト指向プログラミング機構を備えています。
Python は、洗練された文法・動的なデータ型付け・インタープリタであることなどから、
スクリプティングや高速アプリケーション開発(Rapid Application Development: RAD)に理想的なプログラミング言語となっています。
Python Web サイト(https://www.python.org) は、 Python インタープリタと標準ライブラリのソースコードと、
主要プラットフォームごとにコンパイル済みのバイナリファイルを無料で配布しています。
また、Python Web サイトには、無料のサードパーティモジュールやプログラム、ツール、ドキュメントなども紹介しています。
'''

python_2 = '''
Python インタプリタは、簡単に C/C++ 言語などで実装された関数やデータ型を組み込み、拡張できます。
また、アプリケーションのカスタマイズを行う、拡張言語としても適しています。
このチュートリアルは、Python 言語の基本的な概念と機能を、形式ばらずに紹介します。
読むだけではなく、Pythonインタープリタで実際にサンプルを実行すると理解が深まりますが、
サンプルはそれぞれ独立していますので、ただ読むだけでも良いでしょう。
'''

python_3 = '''
標準オブジェクトやモジュールの詳細は、 Python 標準ライブラリを参照してください。
また、正式な言語定義は、Python 言語リファレンスにあります。
C 言語や C++ 言語で拡張モジュールを書くなら、
Python インタプリタの拡張と埋め込み や Python/C API リファレンスマニュアル を参照してください。
Python の解説書も販売されています。
'''

python_4 = '''
このチュートリアルは、Python全体を対象とした、包括的な解説書ではありません。
よく使われる機能に限っても、全ては紹介していません。その代わり、このチュートリアルでは、
Pythonのもっとも特徴的な機能を中心に紹介して、この言語の持ち味や、スタイルを感じられるようにしています。
このチュートリアルを読み終えると、Python のモジュールやプログラムを読み書きできるようになっているでしょう。
また、Python 標準ライブラリ のさまざまな Python ライブラリモジュールを、詳しく調べられるようになっているはずです。
'''

messages_list = [
    split_text_only_noun(python_1),
    split_text_only_noun(python_2),
    split_text_only_noun(python_3),
    split_text_only_noun(python_4),
    # split_text_only_noun('私達はラーメンがとても大好きです。'),
    # split_text_only_noun('私達は蕎麦がとても大好きです。')
]
docs = np.array(messages_list)
print(messages_list)
# print(docs)

# bow ( bag of words )
count = CountVectorizer()
bags = count.fit_transform(docs)
features = count.get_feature_names()

print('bag : ', bags)
print(bags.toarray())
print("count.vocabulary_ : ", count.vocabulary_)
print('features:', features)
print(features)
print("---------------------------------------------------")


# tf-idf
tfidf = TfidfTransformer(use_idf=True, norm='l2', smooth_idf=True)
np.set_printoptions(precision=2)
tf_idf = tfidf.fit_transform(bags)
# print(tf_idf)
# print(tf_idf.toarray())

# cos類似度
# 文書間の類似度
# python_1とpython_2の文書比較
a = tf_idf.toarray()[0]
b = tf_idf.toarray()[1]
print(cos_sim(a, b))
