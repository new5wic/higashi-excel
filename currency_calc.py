import pandas as pd

def load_and_prepare_data(folder_path):
    # データを読み込む
    interbank_rates = pd.read_csv(f'{folder_path}/interbank_currency_rates.csv')
    yahoo_rates = pd.read_csv(f'{folder_path}/yahoo_rates.csv')
    gpa_rates = pd.read_csv(f'{folder_path}/gpa_rate.csv')
    mufg_rates = pd.read_csv(f'{folder_path}/mufg_wc.csv')

    # インターバンクの売り・買いレート分割
    interbank_sell = interbank_rates[interbank_rates['Type'] == 'SELL'].rename(columns={'Rate': 'Interbank_Sell'}).drop(columns='Type')
    interbank_buy = interbank_rates[interbank_rates['Type'] == 'BUY'].rename(columns={'Rate': 'Interbank_Buy'}).drop(columns='Type')

    # 空港と銀行のレート分割
    gpa_rates['Type'] = gpa_rates['Currency'].apply(lambda x: 'SELL' if 'SELL' in x else 'BUY')
    gpa_rates['Currency'] = gpa_rates['Currency'].str.replace('_SELL', '').str.replace('_BUY', '')
    gpa_sell = gpa_rates[gpa_rates['Type'] == 'SELL'].rename(columns={'Price': 'GPA_Sell'}).drop(columns='Type')
    gpa_buy = gpa_rates[gpa_rates['Type'] == 'BUY'].rename(columns={'Price': 'GPA_Buy'}).drop(columns='Type')

    # データ統合
    sell_rates = pd.merge(pd.merge(pd.merge(interbank_sell, gpa_sell, on='Currency', how='outer'), yahoo_rates, on='Currency', how='outer'), mufg_rates[['Currency', 'Sell Rate']], on='Currency', how='outer').rename(columns={'Rate': 'Yahoo', 'Sell Rate': 'MUFG_Sell'})
    buy_rates = pd.merge(pd.merge(pd.merge(interbank_buy, gpa_buy, on='Currency', how='outer'), yahoo_rates, on='Currency', how='outer'), mufg_rates[['Currency', 'Buy Rate']], on='Currency', how='outer').rename(columns={'Rate': 'Yahoo', 'Buy Rate': 'MUFG_Buy'})

    # 利幅の計算と提案価格の算出
    sell_rates['Suggested_Sell_Rate'] = sell_rates[['GPA_Sell', 'MUFG_Sell']].min(axis=1) - 1
    sell_rates['Profit'] = sell_rates['Suggested_Sell_Rate'] - sell_rates['Interbank_Sell']
    
    # Buy Ratesの提案価格算出
    buy_rates['Max_Rate'] = buy_rates[['GPA_Buy', 'MUFG_Buy']].max(axis=1)
    buy_rates['Suggested_Buy_Rate'] = buy_rates.apply(lambda x: min(max(x['Max_Rate'], x['Interbank_Buy'] if pd.notna(x['Interbank_Buy']) else x['Max_Rate']), x['Yahoo']), axis=1)
    buy_rates['Profit'] = buy_rates['Suggested_Buy_Rate'] - buy_rates['Yahoo']

    return sell_rates, buy_rates

def save_to_excel(sell_rates, buy_rates, output_path):
    with pd.ExcelWriter(output_path) as writer:
        sell_rates.to_excel(writer, sheet_name='Sell Rates', index=False)
        buy_rates.to_excel(writer, sheet_name='Buy Rates', index=False)

def main():
    folder_path = 'c:/CSV'  # データフォルダパスを設定
    output_path = 'c:/csv/output/results.xlsx'  # 出力ファイルパスを設定
    sell_rates, buy_rates = load_and_prepare_data(folder_path)
    save_to_excel(sell_rates, buy_rates, output_path)

if __name__ == "__main__":
    main()
