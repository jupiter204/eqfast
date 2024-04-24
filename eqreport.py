import requests
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()
url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization={
    os.getenv('cwatoken')}&limit=1'


def init():
    with open('record1.txt', 'r') as f:
        return int(f.readline())


def get(nb):
    data = requests.get(url)
    data_json = data.json()
    eq = data_json['records']['Earthquake'][0]
    num = eq['EarthquakeNo']
    if nb == num:
        return num, 0, 0, 0, 0, 0, 0, 0
    with open('record1.txt', 'w') as f:
        f.write(f'{num}')
    color = eq['ReportColor']
    msg = eq['ReportContent']
    image = eq['ReportImageURI']
    weburl = eq['Web']
    eq = eq['EarthquakeInfo']
    depth = eq['FocalDepth']
    loc = eq['Epicenter']['Location']
    mag = eq['EarthquakeMagnitude']['MagnitudeValue']
    return num, color, msg, image, weburl, depth, loc, mag


if __name__ == '__main__':
    num = init()
    while True:
        num, color, msg, image, weburl, depth, loc, mag = get(num)
        if msg != 0:
            print(num, color, msg, image, weburl, depth, loc, mag)
        sleep(1)
