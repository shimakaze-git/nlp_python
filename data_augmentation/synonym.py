import os
import sqlite3

from collections import namedtuple


path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')
conn = sqlite3.connect(path + 'wnjpn.db')


def get_synonym_word(word):
    cur = conn.execute("select * from word where lemma=?", (word,))
    word_list = [row for row in cur]
    synonym_list = []
    for word in word_list:
        cur = conn.execute("select * from sense where wordid=?", (word[0],))
        synnet_list = [row for row in cur]
        for synnet in synnet_list:
            cur = conn.execute(
                "select * from sense, word where synset = ? and word.lang = 'jpn' and sense.wordid = word.wordid;", (synnet[0],)
            )
            synonym_list += [row[9] for row in cur]
    return synonym_list


Word = namedtuple('Word', 'wordid lang lemma pron pos')


def getWords(lemma):
    words = []
    cur = conn.execute("select * from word where lemma=?", (lemma,))
    row = cur.fetchone()
    while row:
        words.append(Word(*row))
        row = cur.fetchone()
    return words


def getWord(wordid):
    cur = conn.execute("select * from word where wordid=?", (wordid,))
    return Word(*cur.fetchone())


Sense = namedtuple('Sense', 'synset wordid lang rank lexid freq src')


def getSenses(word):
    senses = []
    cur = conn.execute("select * from sense where wordid=?", (word.wordid,))
    row = cur.fetchone()
    while row:
        senses.append(Sense(*row))
        row = cur.fetchone()
    return senses


def getSense(synset, lang='jpn'):
    cur = conn.execute(
        "select * from sense where synset=? and lang=?", (synset, lang)
    )
    row = cur.fetchone()
    if row:
        return Sense(*row)
    else:
        return None


SynLink = namedtuple('SynLink', 'synset1 synset2 link src')


def getSynLinks(sense, link):
    synLinks = []
    cur = conn.execute(
        "select * from synlink where synset1=? and link=?", (sense.synset, link)
    )
    row = cur.fetchone()
    while row:
        synLinks.append(SynLink(*row))
        row = cur.fetchone()
    return synLinks


def abstract_word(lemma):
    result = []
    for word in getWords(lemma):
        for sense in getSenses(word):
            if sense.src != 'hand':
                continue
            for synlink in getSynLinks(sense, 'hype'):
                abst_sense = getSense(synlink.synset2)
                if abst_sense and word.wordid != abst_sense.wordid:
                    result.append(getWord(abst_sense.wordid).lemma)
    return result


if __name__ == "__main__":
    word = input().rstrip()

    words = []
    words += get_synonym_word(word)
    print(word, words)

    words = []
    words += abstract_word(word)
    print(word, words)
