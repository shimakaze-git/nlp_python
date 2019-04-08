from sklearn.feature_extraction.text import CountVectorizer as CV

msg = '''
Qiitaは「プログラミングに関する知識を記録・共有するためのサービス」ですので、
再利用性・汎用性の高い情報が多く集まっている場をつくっていきたいと考えています。
そのためには、記事を読むこと、記事を書くことを通して、
読む側・書く側それぞれがお互いに関わり合って、
再利用性・汎用性の高い情報を育てていきましょう。
'''

txt = '''
Python is an interpreted high-level programming language for general-purpose programming.
Created by Guido van Rossum and first released in 1991, Python has a design philosophy that emphasizes code readability, and a syntax that allows programmers to express concepts in fewer lines of code,notably using significant whitespace.
It provides constructs that enable clear programming on both small and large scales.
Python features a dynamic type system and automatic memory management.
It supports multiple programming paradigms, including object-oriented, imperative, functional and procedural, and has a large and comprehensive standard library.
Python interpreters are available for many operating systems.
CPython, the reference implementation of Python, is open source software and has a community-based development model, as do nearly all of its variant implementations.
CPython is managed by the non-profit Python Software Foundation.
'''

source_list = []
for x in txt.split('\n'):
    if x is not '':
        source_list.append(x)


# print(source_list)

# cv = CV()
cv = CV(stop_words="english", ngram_range=(1, 2))
matrix = cv.fit_transform(source_list)
print(matrix)

print(cv.get_feature_names())
