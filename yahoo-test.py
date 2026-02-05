import requests
from lxml import html

# テスト対象の通貨と URL（必要に応じて追加・削除してください）
currencies = {
    "USD": "https://finance.yahoo.co.jp/quote/USDJPY=X",
    "EUR": "https://finance.yahoo.co.jp/quote/EURJPY=X",
    "GBP": "https://finance.yahoo.co.jp/quote/GBPJPY=X",
    # …以下省略…
}

# いま手に入れた新しい XPath
xpath = '//*[@id="contents"]/div/section/div[2]/div[2]/div[1]/span/span/span'

for code, url in currencies.items():
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        tree = html.fromstring(resp.content)
        elems = tree.xpath(xpath)
        if elems and elems[0].text:
            print(f"{code} ✅ {elems[0].text.strip()}")
        else:
            print(f"{code} ❌ 要素が見つかりませんでした（XPath 再確認）")
    except Exception as e:
        print(f"{code} ⚠ エラー: {e}")
