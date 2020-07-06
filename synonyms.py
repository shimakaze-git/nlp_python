import sqlite3


def search_similar_words(word):
    conn = sqlite3.connect('wnjpn.db')
    sql = 'select wordid from word where lemma="{}"'.format(word)

    cur = conn.execute(sql)

    # word_idが99999999の場合はwordnetに存在しない単語
    word_id = 99999999  # temp

    for row in cur:
        word_id = row[0]

    # Wordnetに存在する語であるかの判定
    if word_id == 99999999:
        print("「%s」は、Wordnetに存在しない単語です。" % word)
        return
    else:
        print("【「%s」の類似語を出力します】\n" % word)

    sql = 'select synset from sense where wordid="{}"'.format(word_id)

    # 入力された単語を含む概念を検索する
    cur = conn.execute(sql)
    synsets = []
    for row in cur:
        synsets.append(row[0])

    # 概念に含まれる単語を検索して画面出力する
    no = 1
    for synset in synsets:
        sql = 'select name from synset where synset="{}"'.format(synset)
        cur1 = conn.execute(sql)
        for row1 in cur1:
            print("{}つめの概念 : {}".format(no, row1[0]))

        sql = 'select def from synset_def where '
        sql += '(synset="{}" and lang="jpn")'.format(synset)
        cur2 = conn.execute(sql)
        sub_no = 1
        for row2 in cur2:
            print("意味{} : {}".format(sub_no, row2[0]))
            sub_no += 1

        sql = 'select wordid from sense where '
        sql += '(synset="{}" and wordid!={})'.format(synset, word_id)
        cur3 = conn.execute(sql)
        sub_no = 1
        for row3 in cur3:
            target_word_id = row3[0]
            sql = 'select lemma from word '
            sql += 'where wordid={}'.format(target_word_id)
            cur3_1 = conn.execute(sql)
            for row3_1 in cur3_1:
                print("類義語{} : {}".format(sub_no, row3_1[0]))
                sub_no += 1

        print('\n')
        no += 1


if __name__ == '__main__':
    # 標準入力から引数
    word = input().rstrip()

    # 類義語をwordnetから検索
    search_similar_words(word)

# https://qiita.com/pocket_kyoto/items/1e5d464b693a8b44eda5
