import requests
from lxml import html
import os
from datetime import datetime
import pyperclip

# URLと通貨のリスト
currencies = {
    "USD": "https://finance.yahoo.co.jp/quote/USDJPY=X",
    "EUR": "https://finance.yahoo.co.jp/quote/EURJPY=X",
    "GBP": "https://finance.yahoo.co.jp/quote/GBPJPY=X",
    "CNY": "https://finance.yahoo.co.jp/quote/CNYJPY=X",
    "KRW": "https://finance.yahoo.co.jp/quote/KRWJPY=X",
    "TWD": "https://finance.yahoo.co.jp/quote/TWDJPY=X",
    "AUD": "https://finance.yahoo.co.jp/quote/AUDJPY=X",
    "CAD": "https://finance.yahoo.co.jp/quote/CADJPY=X",
    "SGD": "https://finance.yahoo.co.jp/quote/SGDJPY=X",
    "THB": "https://finance.yahoo.co.jp/quote/THBJPY=X",
    "HKD": "https://finance.yahoo.co.jp/quote/HKDJPY=X",
    "PHP": "https://finance.yahoo.co.jp/quote/PHPJPY=X",
    "IDR": "https://finance.yahoo.co.jp/quote/IDRJPY=X",
    "MYR": "https://finance.yahoo.co.jp/quote/MYRJPY=X"
}

# XPathのパス
xpath = '//*[@id="contents"]/div/div[2]/div[2]/div[2]/p[2]/span'

# 通貨名の対応表
currency_names = {
    "USD": "ドル-円",
    "EUR": "ユーロ-円",
    "GBP": "英ポンド-円",
    "CNY": "人民元-円",
    "KRW": "韓国ウォン-円",
    "TWD": "台湾ドル-円",
    "AUD": "オーストラリアドル-円",
    "CAD": "カナダドル-円",
    "SGD": "シンガポールドル-円",
    "THB": "タイバーツ-円",
    "HKD": "香港ドル-円",
    "PHP": "フィリピンペソ-円",
    "IDR": "インドネシアルピア-円",
    "MYR": "マレーシアリンギット-円"
}

# 現在の日時を取得
current_time = datetime.now().strftime('%Y年%m月%d日 %H時%M分抽出')

# ファイルの保存場所を指定
output_directory = r'C:\CSV'
filename = 'yahoo_rates_Excel.txt'
full_path = os.path.join(output_directory, filename)

# ファイルが存在する場合は削除
if os.path.exists(full_path):
    os.remove(full_path)

# データをテキストファイルに保存し、クリップボードにコピー
with open(full_path, 'w', encoding='utf-8') as file:
    clipboard_text = current_time + '\n'  # クリップボード用のテキストを初期化
    file.write(current_time + '\n')
    for currency, url in currencies.items():
        response = requests.get(url)
        tree = html.fromstring(response.content)
        rate = tree.xpath(xpath)[0].text
        line = f"{currency_names[currency]}\n{rate}\n"
        file.write(line)
        clipboard_text += line  # クリップボード用テキストに追加

pyperclip.copy(clipboard_text)  # クリップボードにテキストをコピー
