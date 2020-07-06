import sqlite3
conn = sqlite3.connect('wnjpn.db')

# 含まれるテーブルの確認
sql = 'select name from sqlite_master where type="{}"'.format('table')
cur = conn.execute(sql)
for row in cur:
    print(row)
