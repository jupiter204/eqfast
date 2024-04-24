from time import sleep
from bs4 import BeautifulSoup
import requests
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
}
url = 'https://www.cwa.gov.tw/V8/C/P/PWS/MOD/PWS_LIST.html'


def init():
    with open('record.txt', 'r') as f:
        return f.readline()


def update(time):
    page = requests.get(url, headers=header)
    page.encoding = 'utf-8'
    soup = BeautifulSoup(page.text, 'html.parser')
    shops = soup.find_all("tbody")
    now = shops[0].select('td')[0].text
    if time != now:
        with open('record.txt', 'w') as f:
            f.write(now)  # 發布時間
        msg = shops[0].select('td')[1].text  # 速報訊息
        area = '警報發布地區：'+shops[0].select('td')[2].text  # 發布地區
        return now, msg, area
    return time, 0, 0


if __name__ == "__main__":
    time = init()
    while True:
        time, msg, area = update(time)
        if msg != 0:
            print(msg)
            print(area)
        sleep(1)
