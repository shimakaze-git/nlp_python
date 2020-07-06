# import sys, sqlite3
import sqlite3
from collections import namedtuple
from pprint import pprint

conn = sqlite3.connect('../wnjpn.db')

Word = namedtuple('Word', 'wordid lang lemma pron pos')
print(Word)
