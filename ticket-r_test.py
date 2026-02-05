from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ChromeDriverの設定
service = Service(executable_path=r'C:\chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)

# ページにアクセス
driver.get('https://d-ranger.jp/en/shop/shinjuku/')
try:
    # ページの完全な読み込みを確認
    WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    # データが存在するかチェック
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.shoprate-table tr')))

    # データの抽出
    rows = driver.find_elements(By.CSS_SELECTOR, '.shoprate-table tr')
    for row in rows:
        # ここで各行のデータを処理
        print(row.text)  # とりあえずコンソールに出力

finally:
    driver.quit()

