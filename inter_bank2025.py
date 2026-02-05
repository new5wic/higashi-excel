import requests
from lxml import html
import csv
import os

# URLの設定
url = 'https://www.interbank.co.jp/'
response = requests.get(url)
response.raise_for_status()  # エラーチェック

# レスポンスのエンコーディングを明示的にUTF-8に設定
response.encoding = 'utf-8'

# HTMLを解析
tree = html.fromstring(response.text)

# 通貨セクションを特定（class="subBox"のdiv要素）
currency_sections = tree.xpath('//div[@class="subBox"]')

# データを格納するリスト
currency_data = []

# 各通貨セクションを処理
for section in currency_sections:
    try:
        # 通貨名の取得（h3タグのテキスト）
        currency_name = section.xpath('.//h3/text()')[0].strip()

        # 売値と買値の取得
        rates = section.xpath('.//dl')
        sell_rate = None
        buy_rate = None
        for rate in rates:
            dd_text = rate.xpath('.//dd/text()')[0].strip()
            dt_text = rate.xpath('.//dt/text()')[0].strip()
            if dd_text == 'we sell':
                sell_rate = dt_text
            elif dd_text == 'we buy':
                buy_rate = dt_text

        # 売値と買値が取得できた場合にデータを追加
        if sell_rate and buy_rate:
            currency_data.append([currency_name, "SELL", sell_rate])
            currency_data.append([currency_name, "BUY", buy_rate])
        else:
            print(f"警告: {currency_name} の売値または買値の抽出に失敗しました。")
    except IndexError:
        print(f"警告: 通貨セクションのデータ抽出に失敗しました。")
    except Exception as e:
        print(f"エラー: セクション処理中に問題が発生しました - {str(e)}")

# CSVファイルに保存
output_directory = 'C:/CSV'  # 保存先ディレクトリ（必要に応じて変更）
filename = 'interbank_currency_rates.csv'
full_path = os.path.join(output_directory, filename)

# ディレクトリが存在しない場合は作成
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# 既存ファイルがあれば削除
if os.path.exists(full_path):
    os.remove(full_path)

# CSV書き込み（エンコーディングをUTF-8に設定、BOM付き）
with open(full_path, 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['Currency', 'Type', 'Rate'])  # ヘッダー
    for data in currency_data:
        writer.writerow(data)

print("データ抽出が完了しました。")