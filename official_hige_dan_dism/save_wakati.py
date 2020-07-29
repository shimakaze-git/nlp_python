import re
import MeCab
import requests

from bs4 import BeautifulSoup


# 文章を読み込む
def read_doc(path='lyrics.txt'):
    text = ""
    with open(path, 'r', errors='ignore') as f:
        text += f.read()
    return text


# データの前処理
def preprocessing(text):
    # 英数字の削除
    text = re.sub("[a-xA-Z0-9_]", "", text)
    # 記号の削除
    text = re.sub("[!-/:-@[-`{-~*]", "", text)
    # 空白・改行の削除
    text = re.sub(u'\n\n', '\n', text)
    text = re.sub(u'\r', '', text)

    return text


# ストップワードリストの生成
def create_stop_word():
    target_url = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
    r = requests.get(target_url)
    soup = BeautifulSoup(r.text, "html.parser")
    stop_word = str(soup).split()

    my_stop_word = [
        'いる', 'する', 'させる', 'の', 'られる'
    ]
    stop_word.extend(my_stop_word)

    return stop_word


# MeCab による単語への分割関数 (名詞のみ残す)
def split_text_only_noun(text):
    stop_word = create_stop_word()

    option = '-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd'
    # option = ''
    tagger = MeCab.Tagger("-Ochasen " + option)
    tagger.parse('')

    # Execute class analysis
    node = tagger.parseToNode(text)

    words = []
    while node:
        # word = node.surface.upper()
        # 基本形を使用する
        word = node.feature.split(',')[6]
        word = word.upper()

        class_feature = node.feature.split(',')[0]
        sub_class_feature = node.feature.split(',')[1]

        # features = ['名詞', '動詞', '形容詞']
        features = ['名詞', '動詞', '形容詞', '形容動詞']
        if class_feature in features:
            if sub_class_feature not in ['空白', '*']:
                # ストップワードに該当しない瀕死を保存する
                if word not in stop_word:
                    words.append(word)
        node = node.next
    return words


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

    # 歌詞を読み込む
    lyrics = read_doc()

    # データの前処理 クリーニング作業
    lyrics = preprocessing(lyrics)

    # 形態素解析
    list_text = split_text_only_noun(lyrics)

    # 分かち書きしたものを保存
    save_wakati_file(list_text)
