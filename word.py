import os
import sqlite3

path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
conn = sqlite3.connect(path + '/' + 'wnjpn.db')


def chk_word():
    sql = "select * from word where lang='jpn' limit 240000"
    cur = conn.execute(sql)
    for row in cur:
        print(row[2])


if __name__ == "__main__":
    chk_word()
