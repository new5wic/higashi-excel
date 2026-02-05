import requests
from lxml import html
import csv
import os

# URLを指定
url = "https://www.gpa-net.co.jp/ja/passenger-service/rate/"

# SSL証明書の検証を無効にしてリクエストを送信
response = requests.get(url, verify=False)  # SSL証明書の検証を無効にすることを確認

# 応答からHTMLを解析
tree = html.fromstring(response.content)

# 各通貨のレートに対応するXPath
xpaths = {
    "USD_SELL": "//td[@class='table-td2'][contains(text(), 'アメリカ ドル')]/following-sibling::td[@class='table-td3']",
    "USD_BUY": "//td[@class='table-td2'][contains(text(), 'アメリカ ドル')]/following-sibling::td[@class='table-td4']",
    "CAD_BUY": "//td[contains(., 'カナダ ドル')]/following-sibling::td[@class='table-td4']",
    "CAD_BUY": "//td[contains(., 'カナダ ドル')]/following-sibling::td[@class='table-td4']",
    "EUR_SELL": "(//td[contains(text(), 'ヨーロッパ')]/following-sibling::td[contains(.//img/@src, 'icon_eu')]/following-sibling::td[@class='table-td3'])[1]",
    "EUR_BUY": "(//td[contains(text(), 'ヨーロッパ')]/following-sibling::td[contains(.//img/@src, 'icon_eu')]/following-sibling::td[@class='table-td4'])[1]",
    "GBP_SELL": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[2]/tr[2]/td[3]",
    "GBP_BUY": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[2]/tr[2]/td[4]",
    "KRW_SELL": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[3]/tr[1]/td[4]",
    "KRW_BUY": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[3]/tr[1]/td[5]",
    "CNY_SELL": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[3]/tr[2]/td[3]",
    "CNY_BUY": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[3]/tr[2]/td[4]",
    "TWD_SELL": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[3]/tr[3]/td[3]",
    "TWD_BUY": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[3]/tr[3]/td[4]",
    "HKD_SELL": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[3]/tr[4]/td[3]",
    "HKD_BUY": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[3]/tr[4]/td[4]",
    "SGD_SELL": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[3]/tr[5]/td[3]",
    "SGD_BUY": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[3]/tr[5]/td[4]",
    "THB_SELL": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[3]/tr[6]/td[3]",
    "THB_BUY": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[3]/tr[6]/td[4]",
    "MYR_SELL": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[3]/tr[7]/td[3]",
    "MYR_BUY": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[3]/tr[7]/td[4]",
    "IDR_SELL": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[3]/tr[8]/td[3]",
    "IDR_BUY": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[3]/tr[8]/td[4]",
    "PHP_SELL": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[3]/tr[9]/td[3]",
    "PHP_BUY": "/html/body/div[1]/main/article/div/section[1]/div[2]/div[2]/div/table/tbody[3]/tr[9]/td[4]",
}


# CSVデータを保存するためのリスト
csv_data = [("Currency", "Price")]

# 各通貨のレートを抽出
for key, xpath in xpaths.items():
    price = tree.xpath(xpath)[0].text.strip()
    csv_data.append((key, price))

# ファイルの保存場所を指定
output_directory = r'C:\CSV'  # Windowsの場合、パスはこのように指定
filename = 'gpa_rate.csv'
full_path = os.path.join(output_directory, filename)

# データをCSVファイルに保存
with open(full_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)
