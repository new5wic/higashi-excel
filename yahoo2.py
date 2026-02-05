import time
import requests
import pyperclip
from lxml import html

# URLリスト
url_list = [
    'https://finance.yahoo.co.jp/quote/USDJPY=X',
    'https://finance.yahoo.co.jp/quote/EURJPY=X',
    'https://finance.yahoo.co.jp/quote/CNYJPY=X',
    'https://finance.yahoo.co.jp/quote/KRWJPY=X',
    'https://finance.yahoo.co.jp/quote/TWDJPY=X',
    'https://finance.yahoo.co.jp/quote/AUDJPY=X',
    'https://finance.yahoo.co.jp/quote/GBPJPY=X',
    'https://finance.yahoo.co.jp/quote/CADJPY=X',
    'https://finance.yahoo.co.jp/quote/SGDJPY=X',
    'https://finance.yahoo.co.jp/quote/THBJPY=X',
    'https://finance.yahoo.co.jp/quote/HKDJPY=X',
    'https://finance.yahoo.co.jp/quote/PHPJPY=X',
    'https://finance.yahoo.co.jp/quote/IDRJPY=X',
    'https://finance.yahoo.co.jp/quote/MYRJPY=X'
]

# 抽出したいXPath
xpath_expression = '//*[@id="contents"]/div/div[2]/div[2]/div[2]/p[2]'

# 結果を保持するリスト
result = []

# URLごとにアクセスして抽出
for url in url_list:
    try:
        response = requests.get(url)
        response.raise_for_status()  # ステータスコードが200でない場合に例外を発生させる
        
        tree = html.fromstring(response.content)
        elements = tree.xpath(xpath_expression)
        
        if elements:
            price = elements[0].text_content().strip()
        else:
            price = "N/A"
            print(f"価格情報を取得できませんでした: {url}")
        
        # 結果をリストに追加
        result.append(price)
    except requests.exceptions.RequestException as e:
        print(f"リクエストエラー: {e}")
        result.append("N/A")
    
    # 2秒待機
    time.sleep(2)

# 結果を整形して表示
timestamp = time.strftime("%Y年%m月%d日 %H時%M分")
output = [timestamp + ' 抽出結果']
output.append('ドル-円')
output.append(result[0])
output.append('ユーロ-円')
output.append(result[1])
output.append('人民元-円')
output.append(result[2])
output.append('韓国ウォン-円')
output.append(result[3])
output.append('台湾ドル-円')
output.append(result[4])
output.append('オーストラリアドル-円')
output.append(result[5])
output.append('英ポンド-円')
output.append(result[6])
output.append('カナダドル-円')
output.append(result[7])
output.append('シンガポールドル-円')
output.append(result[8])
output.append('タイバーツ-円')
output.append(result[9])
output.append('香港ドル-円')
output.append(result[10])
output.append('フィリピンペソ-円')
output.append(result[11])
output.append('インドネシアルピア-円')
output.append(result[12])
output.append('マレーシアリンギット-円')
output.append(result[13])

# 結果をクリップボードにコピー
result_text = '\n'.join(output)
pyperclip.copy(result_text)

# 結果を表示
for line in output:
    print(line)
