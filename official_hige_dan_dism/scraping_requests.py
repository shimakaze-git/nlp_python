import time
import re
import requests

from bs4 import BeautifulSoup


def requests_get(url):
    res = requests.get(url)
    res.raise_for_status()

    return res.text


def pickup_tag(html, tag):
    soup = BeautifulSoup(str(html), 'html.parser')
    paragraphs = soup.find_all(tag)

    return paragraphs


def get_song_url(html):
    song_url = []

    base_url = 'https://www.uta-net.com'

    ''' 曲のurlを取得 '''
    # td要素の取り出し
    for td in pickup_tag(html, 'td'):
        # a要素の取り出し
        for a in pickup_tag(td, 'a'):
            # href属性にsongを含むか
            if 'song' in a.get('href'):
                # urlを配列に追加
                song_url.append(base_url + a.get('href'))

    return song_url


def get_lyrics(song_url):
    ''' 歌詞の取得 '''

    # 歌詞を格納
    lyrics = ''
    for i, page in enumerate(song_url):
        print('{}曲目:{}'.format(i + 1, page))

        res_text = requests_get(page)
        soup = BeautifulSoup(res_text, 'html')

        # 歌詞の'itemprop="text"'がある所
        soup = soup.find('div', itemprop='lyrics')
        soup = soup.find('div', itemprop='text')

        # htmlタグの排除
        song_lyrics = soup.getText()
        song_lyrics = song_lyrics.replace('\n', '')
        song_lyrics = song_lyrics.replace('　', '')

        # 英数字の排除
        song_lyrics = re.sub(r'[a-zA-Z0-9]', '', song_lyrics)
        # 記号の排除
        song_lyrics = re.sub(
            r'[ ＜＞♪`‘’“”・…_！？!-/:-@[-`{-~]', '', song_lyrics
        )

        # 注意書きの排除
        song_lyrics = re.sub(r'注意：.+', '', song_lyrics)

        # 歌詞を1つにまとめる
        lyrics += song_lyrics + '\n'

        time.sleep(1)
    return lyrics


def main(artist_url):
    res_text = requests_get(artist_url)

    ''' 曲のurlを取得 '''
    song_url = get_song_url(res_text)

    ''' 歌詞を取得する '''
    lyrics = get_lyrics(song_url)

    # lyrics.txtに歌詞を保存
    with open('./lyrics.txt', mode='a') as f:
        f.write(lyrics)


if __name__ == "__main__":
    artist_url = 'https://www.uta-net.com/artist/18093/'
    main(artist_url)
