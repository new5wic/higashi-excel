import requests
from lxml import html
import csv
import os  # osモジュールをインポート

# URLと通貨のリスト
currencies = {
    "USD": "https://finance.yahoo.co.jp/quote/USDJPY=X",
    "EUR": "https://finance.yahoo.co.jp/quote/EURJPY=X",
    "GBP": "https://finance.yahoo.co.jp/quote/GBPJPY=X",
    "CNY": "https://finance.yahoo.co.jp/quote/CNYJPY=X",
    "AUD": "https://finance.yahoo.co.jp/quote/AUDJPY=X",
    "CAD": "https://finance.yahoo.co.jp/quote/CADJPY=X",
    "SGD": "https://finance.yahoo.co.jp/quote/SGDJPY=X",
    "KRW": "https://finance.yahoo.co.jp/quote/KRWJPY=X",
    "HKD": "https://finance.yahoo.co.jp/quote/HKDJPY=X",
    "TWD": "https://finance.yahoo.co.jp/quote/TWDJPY=X",
    "THB": "https://finance.yahoo.co.jp/quote/THBJPY=X",
    "PHP": "https://finance.yahoo.co.jp/quote/PHPJPY=X",
    "IDR": "https://finance.yahoo.co.jp/quote/IDRJPY=X",
    "MYR": "https://finance.yahoo.co.jp/quote/MYRJPY=X"
}

# XPathのパス
xpath = '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/p[2]/span'

# CSVデータを保存するためのリスト
csv_data = [("Currency", "Rate")]

# 各通貨についてスクレイピング
for currency, url in currencies.items():
    response = requests.get(url)
    tree = html.fromstring(response.content)
    rate = tree.xpath(xpath)[0].text
    csv_data.append((currency, rate))

# ファイルの保存場所を指定
output_directory = r'C:\CSV'  # raw stringを使用
filename = 'yahoo_rates.csv'
full_path = os.path.join(output_directory, filename)

# ファイルが存在する場合は削除
if os.path.exists(full_path):
    os.remove(full_path)

# データをCSVファイルに保存
with open(full_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)  # `writerows`を使用して全データを一度に書き込む
