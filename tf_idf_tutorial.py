#!/usr/bin/env python

# 1.データセットの取得
# 1-1.モジュールのインポート
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# 1-2.twenty_trainという変数にデータセット（トレーニング用）を格納
twenty_train = fetch_20newsgroups(
    subset='train', shuffle=True, random_state=42
)

# print(twenty_train)
# print(type(twenty_train))
# print(fetch_20newsgroups)

# 2.データの確認(チュートリアルには記載なし)
print("=====2.データの確認=====")

# 2-1.カテゴリの確認(どんなカテゴリがあるのか。)
print(twenty_train.target_names)
# 2-2.何本のニュースデータがあるのか（11,314本のニュースデータ）
print(len(twenty_train.data))
# 2-3.データ型を確認(list)
print(type(twenty_train.data))
# 2-4.リストの中のデータ型を確認(str)
print(type(twenty_train.data[0]))

print("[実際にデータの中身を確認]")
# 2-5.実際に1本ニュースを確認する(カテゴリ名)
print(twenty_train.target_names[twenty_train.target[10]])
# 2-6.実際に1本ニュースを確認する(ニュースの中身)
print("\n".join(twenty_train.data[10].split("\n")[:15]))

'''
今回はこのデータセットを、「twenty_train」という変数に格納します。
このデータセットから、さらに「target_names」、「data」、「target」の３つが確認できます。それぞれのデータの中身については下記の通り。
target_names:　各ニュースカテゴリ名
data: ニュースデータ
target: ニュースカテゴリのIDのようなもの。target_namesに格納されているニュースカテゴリ名を引き出す際に利用。
'''

# 3.絞り込み
print("=====3.絞り込み=====")

# 3-1.今回分析対象とするカテゴリーを絞り込む
categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']

# 3-2.上記で絞り込んだカテゴリーのデータのみを変数に入れる
twenty_train = fetch_20newsgroups(
    subset='train', categories=categories, shuffle=True, random_state=42
)
# 3-3.カテゴリの確認(ちゃんと絞り込めているか。)
print(twenty_train.target_names)
# 3-4.絞り込んだ結果、ニュースデータが何本になったか（2,257本のニュースデータ）
print(len(twenty_train.data))
# 3-5.データの内容を確認
print("\n".join(twenty_train.data[0].split("\n")[:3]))
# 3-6.データのカテゴリーを確認
print(twenty_train.target_names[twenty_train.target[0]])

# 4.カテゴリ名を確認
print('=====4.カテゴリ名を確認=====')

# 4-1.上から10個のデータのカテゴリーを確認する（カテゴリーID）
print(twenty_train.target[:10])
# 4-2.カテゴリーの意味がわからないので確認する（target_namesに格納されている）
for t in twenty_train.target[:10]:
    print(twenty_train.target_names[t])

# 5.テキストのトークン化とBoW計算(単語の出現頻度をカウント)
print("=====5.テキストのトークン化とBoW計算=====")

# 5-2.モジュールを使うための準備
count_vect = CountVectorizer()
# 5-3.単語の出現頻度をカウント(BoW)!!!!!
X_train_counts = count_vect.fit_transform(twenty_train.data)

# 5-4.BoWの計算結果を保持した変数のデータを確認
print(type(X_train_counts))
# 5-5.BoWの計算結果を保持した変数のデータを確認
print(X_train_counts.shape)
# 5-6.BoWの計算結果を保持した変数のデータを確認（疎行列）
print(X_train_counts.todense())
# 5-7.どのような形態素があったのかを見る(
# こういうこともできるよ、という紹介です。実行すると大量の形態素が表示されるので実行する際はご注意ください
# )
# print(count_vect.get_feature_names())

# 5-8.疎行列の中の実際の値を確認
print(X_train_counts[0])
# 5-9.'algorithm'という単語のインデックス値を確認
print(count_vect.vocabulary_.get(u'algorithm'))


# 6.tf-idfの計算
print("=====6.tf-idfの計算=====")

tfidf_transformer = TfidfTransformer()
# 6-1.BoWの計算結果から、tf-idfを計算
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

# 6-2.計算結果がどんな形になっているかを確認
print(type(X_train_tfidf))
# 6-3.計算結果がどんな形になっているかを確認
print(X_train_tfidf.shape)
# 6-4.計算の結果、どのようになったのかを見てみる（5-6と値のみが異なる）
print(X_train_tfidf.todense())
# 6-5.BoWからtf-idfっぽい数字になっているかを確認
print(X_train_tfidf[0])
