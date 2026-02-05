from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# ChromeDriverのパス
chrome_driver_service = Service(executable_path=r'C:\chromedriver.exe')  # 正しいパスに更新してください

# WebDriverの設定
options = webdriver.ChromeOptions()
options.add_argument('--headless')

# Serviceオブジェクトを使ってWebDriverを起動
driver = webdriver.Chrome(service=chrome_driver_service, options=options)

# 対象ページにアクセス
driver.get('https://d-ranger.jp/en/shop/shinjuku/')

# ページのJavaScriptが完全にロードされるまで待機
WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

# 要素がロードされるまで待機
wait = WebDriverWait(driver, 6)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.shoprate-table')))

# データを抽出
currency_elements = driver.find_elements(By.CSS_SELECTOR, '.shoprate-name')
buy_elements = driver.find_elements(By.CSS_SELECTOR, '.cell-buy')
sell_elements = driver.find_elements(By.CSS_SELECTOR, '.cell-sell')

# CSVファイルに保存
with open('d-ranger.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['currency', 'buy', 'sell'])  # ヘッダーを書き込む

    # 各通貨ごとに繰り返し
    for currency, buy, sell in zip(currency_elements, buy_elements, sell_elements):
        currency_name = currency.text.split('\n')[1]  # 通貨名を抽出
        buy_rate = buy.text.split(' ')[0]  # 購入レートを抽出
        sell_rate = sell.text.split(' ')[0]  # 売却レートを抽出
        writer.writerow([currency_name, buy_rate, sell_rate])  # データを書き込む

# WebDriverを閉じる
driver.quit()


