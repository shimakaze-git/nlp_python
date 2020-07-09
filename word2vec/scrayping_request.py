from bs4 import BeautifulSoup as bs
import requests


def request_bs_soup(url):
    # Responseオブジェクトの取得
    response = requests.get(url)
    soup = bs(response.text.encode(response.encoding), 'html.parser')
    return soup
