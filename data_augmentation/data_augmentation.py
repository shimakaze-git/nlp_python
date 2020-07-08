import MeCab
from synonym import get_synonym_word, abstract_word

mecab = MeCab.Tagger("-Ochasen")
mecab.parse('')

words_list = []


# テキストの水増し
def data_augmentation_for_text(sentence):
    sentence_list_origin = []
    nodes = word_and_class(sentence)
    print('nodes', nodes)
    get_word(nodes, sentence_list=sentence_list_origin)
    return sentence_list_origin


# 単語を名詞か形容詞などに分類する
def word_and_class(doc):
    doc_ex = doc

    # Execute class analysis
    node = mecab.parseToNode(doc_ex)

    # Extract word and class
    word_class = []
    while node:
        word = node.surface
        class_feature = node.feature.split(',')[0]
        if class_feature != 'BOS/EOS':
            word_class.append((word, class_feature))
        node = node.next
    return word_class


# 単語の取得
def get_word(nodes, index=0, sentence="", sentence_list=[]):
    if len(nodes) == index:
        if sentence not in sentence_list:
            sentence_list.append(sentence)
        return None

    next_index = index + 1
    if nodes[index][1] == "副詞" or nodes[index][1] == "形容詞":
        get_word(
            nodes,
            index=next_index,
            sentence=sentence,
            sentence_list=sentence_list
        )
        get_word(
            nodes,
            index=next_index,
            sentence=sentence + nodes[index][0],
            sentence_list=sentence_list
        )

    elif nodes[index][1] == "名詞":
        candidate_words = []
        candidate_words += get_synonym_word(nodes[index][0])
        candidate_words += abstract_word(nodes[index][0])

        get_word(
            nodes,
            next_index,
            sentence + nodes[index][0],
            sentence_list=sentence_list
        )
        for candidate_word in candidate_words:
            get_word(
                nodes,
                next_index,
                sentence + candidate_word,
                sentence_list=sentence_list
            )
    else:
        get_word(
            nodes,
            next_index,
            sentence + nodes[index][0],
            sentence_list=sentence_list
        )


if __name__ == "__main__":
    # sample_sentence = '隣の柿はよく柿食う客だ'
    sample_sentence = input().rstrip()
    sentence_list = data_augmentation_for_text(sample_sentence)

    for i, sentence in enumerate(sentence_list):
        print('sentense', i, sentence)
