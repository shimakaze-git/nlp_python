import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


# bow ( bag of words )
min_df = 0.24
max_df = 0.76
count = CountVectorizer()
# count = CountVectorizer(min_df, max_df, stop_words="english")

messages_list = [
    'The sun is shining',
    'The weather is shining',
    'the sun is shining, the weather is sweet, and one and one is two'
]
docs = np.array(messages_list)
bag = count.fit_transform(docs)

print(bag)
print(bag.toarray())
print(count.vocabulary_)
print(count.get_feature_names())


# tf-idf
tfidf = TfidfTransformer(use_idf=True, norm='l2', smooth_idf=True)
np.set_printoptions(precision=2)
tf_idf = tfidf.fit_transform(count.fit_transform(docs))
print(tf_idf)
print(tf_idf.toarray())
