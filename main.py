from bs4 import BeautifulSoup
import requests
import codecs
import datetime


def check_wiki_link(link):
    if link[1] == "w"\
            and link[2] == "i"\
            and link[3] == "k"\
            and link[4] == "i"\
            and link[6] == "%":
        return True
    return False


def check_title(link_title):
    if link_title[-1] != "]" and ":" not in link_title:
        return True
    return False


def get_date_data(
):
    today_data: datetime.date = datetime.date.today()
    date_data: str = "{year}_{month}_{day}".format(
        year="0" + str(today_data.year) if today_data.year < 10 else str(today_data.year),
        month="0" + str(today_data.month) if today_data.month < 10 else str(today_data.month),
        day="0" + str(today_data.day) if today_data.day < 10 else str(today_data.day)
    )
    return date_data


url = 'https://ja.wikipedia.org/wiki/メインページ'
# urlを特定の記事のページのものに差し替えればそのページのリンク一覧を取得可能です。
html = requests.get(url)
soup = BeautifulSoup(html.text, 'lxml')
title_list = ""
for a in soup.find_all('a'):
    href = a.get("href")
    title = a.get("title")
    if title is None or href is None:
        # ページ内リンクやリンク先のタイトルが存在しないリンクを除外
        continue
    if "wiki" in href:
        # wikiのサーバー内のリンクかどうかを検出
        if check_wiki_link(href):
            if check_title(title):
                # andにするとエラーが出るケースが出たので二重にif文を記述
                title_list += (title+"\n")
print(title_list)
try:
    with codecs.open(filename="./log/{}.txt".format(get_date_data()), mode="w", encoding="utf-8") as f:
        f.write(title_list)
        # 保存
except Exception as write_error:
    print(write_error)
    # なぜかここでエラーが多発したのでエラーチェック
