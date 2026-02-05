import os
import requests
from lxml import html
from datetime import datetime
import pyperclip
import configparser

# --- ① 設定ファイル読み込み ---
CONFIG_PATH = r'C:\CSV\settings.ini'
DEFAULT_XPATH = '//*[@id="contents"]/div/section/div[2]/div[2]/div[1]/span/span/span'

config = configparser.ConfigParser()
if os.path.exists(CONFIG_PATH):
    config.read(CONFIG_PATH, encoding='utf-8')

xpath = config['DEFAULT'].get('xpath', DEFAULT_XPATH)

# --- ② 取得対象の通貨と URL 定義 ---
currencies = {
    "USD": "https://finance.yahoo.co.jp/quote/USDJPY=X",
    "EUR": "https://finance.yahoo.co.jp/quote/EURJPY=X",
    "CNY": "https://finance.yahoo.co.jp/quote/CNYJPY=X",
    "KRW": "https://finance.yahoo.co.jp/quote/KRWJPY=X",
    "TWD": "https://finance.yahoo.co.jp/quote/TWDJPY=X",
    "AUD": "https://finance.yahoo.co.jp/quote/AUDJPY=X",
    "GBP": "https://finance.yahoo.co.jp/quote/GBPJPY=X",
    "CAD": "https://finance.yahoo.co.jp/quote/CADJPY=X",
    "SGD": "https://finance.yahoo.co.jp/quote/SGDJPY=X",
    "THB": "https://finance.yahoo.co.jp/quote/THBJPY=X",
    "HKD": "https://finance.yahoo.co.jp/quote/HKDJPY=X",
    "PHP": "https://finance.yahoo.co.jp/quote/PHPJPY=X",
    "IDR": "https://finance.yahoo.co.jp/quote/IDRJPY=X",
    "MYR": "https://finance.yahoo.co.jp/quote/MYRJPY=X"
}

currency_names = {
    "USD": "ドル-円",
    "EUR": "ユーロ-円",
    "CNY": "人民元-円",
    "KRW": "韓国ウォン-円",
    "TWD": "台湾ドル-円",
    "AUD": "オーストラリアドル-円",
    "GBP": "英ポンド-円",
    "CAD": "カナダドル-円",
    "SGD": "シンガポールドル-円",
    "THB": "タイバーツ-円",
    "HKD": "香港ドル-円",
    "PHP": "フィリピンペソ-円",
    "IDR": "インドネシアルピア-円",
    "MYR": "マレーシアリンギット-円"
}

# --- ③ 出力先ディレクトリとファイルパス ---
output_dir = r'C:\CSV'
os.makedirs(output_dir, exist_ok=True)
full_path = os.path.join(output_dir, 'yahoo_rates_Excel.txt')

# --- ④ 抽出日時ヘッダー ---
header = datetime.now().strftime('%Y年%m月%d日 %H時%M分') + ' 抽出結果'

# --- ⑤ データ抽出・リスト化 ---
lines = [header]
for code, url in currencies.items():
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        tree = html.fromstring(resp.content)
        elems = tree.xpath(xpath)
        if elems and elems[0].text:
            rate = elems[0].text.strip()
        else:
            rate = "xpath変更の可能性があります。C:\CSV\setting.ini内のxpathを変更してください"
            print(f"[Warning] {code} の要素が見つかりませんでした。")
    except Exception as e:
        rate = "xpath変更の可能性があります"
        print(f"[Error] {code} の取得で例外発生: {e}")

    lines.append(currency_names[code])
    lines.append(rate)

# --- ⑥ 空行を除去 & テキスト結合（末尾改行なし）---
filtered = [ln for ln in lines if ln.strip()]
text = "\n".join(filtered)

# --- ⑦ ファイル書き込み & クリップボードコピー ---
with open(full_path, 'w', encoding='utf-8') as f:
    f.write(text)

pyperclip.copy(text)
print("出力完了:", full_path)
