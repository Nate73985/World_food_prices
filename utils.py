import requests, csv


class DataExtraction:
    def __init__(self, csv_file, output_csv_file, url, base_currency="USD_Amount"):
        self.csv_file = csv_file
        self.output_csv_file = output_csv_file
        self.url = url
        self.base_currency = base_currency
        
    def convert_to_usd(self, amount, rate):
        return amount * rate

    def download(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            data = response.json()
            rates = data['rates']
            return rates
        else:
            print(f"Error fetching exchange rates. Status code: {response.status_code}")
            exit(1)


    def read_data(self, local=False):
        with open(self.csv_file, 'r') as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames + [self.base_currency]  # Update fieldnames to include 'USD Amount'
            rows = list(reader)

            rates = self.download()
            for row in rows:
                amount = float(row['mp_price'])
                currency = row['cur_name']

                if currency in rates:
                    usd_amount = self.convert_to_usd(amount, rates[currency])
                    row['USD Amount'] = usd_amount
                else:
                    print(f"Exchange rate for currency {currency} is not available.")
        
        if local:
            with open(self.output_csv_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            print(f"Conversion completed. USD amounts saved to '{output_csv_file}'.")
        else:
            pass # write a function to write to s3
        
def read_from_s3():
    #read from s3
    return df