import requests
from lxml import html
import csv
import os

# URLの設定
url = 'https://www.interbank.co.jp/'

# HTTPリクエストを送信
response = requests.get(url)
response.raise_for_status()  # HTTPエラーがあれば例外を発生

# HTMLをlxmlで解析
tree = html.fromstring(response.content)

# XPathの定義(現在は年末版)
xpaths = {
    'USD_SELL': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/dl[1]/dt',
    'USD_BUY': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/dl[2]/dt',
    'EUR_SELL': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[1]/div/div[2]/div[1]/div[2]/dl[1]/dt',
    'EUR_BUY': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[1]/div/div[2]/div[1]/div[2]/dl[2]/dt',
    'CNY_SELL': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[1]/div/div[3]/div[1]/div[2]/dl[1]/dt',
    'CNY_BUY': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[1]/div/div[3]/div[1]/div[2]/dl[2]/dt',
    'KRW_SELL': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[2]/div/div[1]/div[1]/div[2]/dl[1]/dt',
    'KRW_BUY': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[2]/div/div[1]/div[1]/div[2]/dl[2]/dt',
    'HKD_SELL': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[2]/div/div[2]/div[1]/div[2]/dl[1]/dt',
    'HKD_BUY': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[2]/div/div[2]/div[1]/div[2]/dl[2]/dt',
    'TWD_SELL': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[2]/div/div[3]/div[1]/div[2]/dl[1]/dt',
    'TWD_BUY': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[2]/div/div[3]/div[1]/div[2]/dl[2]/dt',
    'GBP_SELL': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[3]/div/div[1]/div[1]/div[2]/dl[1]/dt',
    'GBP_BUY': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[3]/div/div[1]/div[1]/div[2]/dl[2]/dt',
    'CAD_SELL': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[3]/div/div[2]/div[1]/div[2]/dl[1]/dt',
    'CAD_BUY': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[3]/div/div[2]/div[1]/div[2]/dl[2]/dt',
    'AUD_SELL': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[3]/div/div[3]/div[1]/div[2]/dl[1]/dt',
    'AUD_BUY': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[3]/div/div[3]/div[1]/div[2]/dl[2]/dt',
    'NZD_SELL': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[4]/div/div[1]/div[1]/div[2]/dl[1]/dt',
    'NZD_BUY': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[4]/div/div[1]/div[1]/div[2]/dl[2]/dt',
    'SGD_SELL': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[4]/div/div[2]/div[1]/div[2]/dl[1]/dt',
    'SGD_BUY': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[4]/div/div[2]/div[1]/div[2]/dl[2]/dt',
    'THB_SELL': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[4]/div/div[3]/div[1]/div[2]/dl[1]/dt',
    'THB_BUY': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[4]/div/div[3]/div[1]/div[2]/dl[2]/dt',
    'PHP_SELL': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[5]/div/div[1]/div[1]/div[2]/dl[1]/dt',
    'PHP_BUY': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[5]/div/div[1]/div[1]/div[2]/dl[2]/dt',
    'VND_SELL': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[5]/div/div[2]/div[1]/div[2]/dl[1]/dt',
    'VND_BUY': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[5]/div/div[2]/div[1]/div[2]/dl[2]/dt',
    'MYR_SELL': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[5]/div/div[3]/div[1]/div[2]/dl[1]/dt',
    'MYR_BUY': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[5]/div/div[3]/div[1]/div[2]/dl[2]/dt',
    'CHF_SELL': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[6]/div/div[1]/div[1]/div[2]/dl[1]/dt',
    'CHF_BUY': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[6]/div/div[1]/div[1]/div[2]/dl[2]/dt',
    'IDR_SELL': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[6]/div/div[2]/div[1]/div[2]/dl[1]/dt',
    'IDR_BUY': '/html/body/div[5]/div[5]/div[1]/div[3]/em/div/div[3]/div[6]/div/div[2]/div[1]/div[2]/dl[2]/dt',
}

# レートをXPathを使って抽出するためのリストを初期化
currency_data = []

for name, path in xpaths.items():
    try:
        rate = tree.xpath(path + '/text()')
        if rate:
            currency_data.append([name.split('_')[0], name.split('_')[1], rate[0].strip()])
    except Exception as e:
        print(f"Error processing {name}: {str(e)}")

# ファイルの保存場所を指定
output_directory = 'C:\CSV'  # 保存したいパスに変更してください
filename = 'interbank_currency_rates.csv'
full_path = os.path.join(output_directory, filename)

# ファイルが存在する場合は削除
if os.path.exists(full_path):
    os.remove(full_path)

# データをCSVファイルに保存
with open(full_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Currency', 'Type', 'Rate'])
    for data in currency_data:
        writer.writerow(data)
