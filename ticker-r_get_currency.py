import requests
from bs4 import BeautifulSoup
import csv

# URL of the webpage to scrape
url = "https://d-ranger.jp/en/shop/shinjuku/"

# Send a request to the webpage
response = requests.get(url)
response.raise_for_status()  # Ensure the request was successful

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Use the correct CSS selector to select the table
table = soup.select_one('.shoprate-table')

# Prepare the list for headers
headers = ['Currency', 'Buy Rate', 'Sell Rate']

# Prepare a list to hold all the data rows
data_rows = []

# Iterate over each row in the table
for row in table.tbody.find_all('tr'):
    # Extract currency name and get only the last 3 characters
    currency_name = row.find('p', class_='shoprate-name').text.strip()[-3:]
    # Extract buy and sell rates and remove any non-numeric characters
    buy_rate = row.find('td', class_='cell-buy').text.strip().split(' ')[0]
    sell_rate = row.find('td', class_='cell-sell').text.strip().split(' ')[0]
    # Clean up rates to remove any non-digit characters (keep decimal points)
    buy_rate = ''.join(filter(lambda x: x.isdigit() or x=='.', buy_rate))
    sell_rate = ''.join(filter(lambda x: x.isdigit() or x=='.', sell_rate))
    # Append to data rows
    data_rows.append([currency_name, buy_rate, sell_rate])

# Define the file path and name
file_path = 'C:/CSV/d-ranger.csv'

# Write the data to a CSV file
with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Write the header
    writer.writerows(data_rows)  # Write the data rows

print("Data has been successfully scraped and saved to", file_path)
