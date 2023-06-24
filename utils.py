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


def labeled_barplot(data, feature, perc=False, n=None):
    total = len(data[feature])
    count = data[feature].nunique()
    if n is None:
        plt.figure(figsize=(count + 1, 5))
    else:
        plt.figure(figsize=(n + 1, 5))

    plt.xticks(rotation=90, fontsize=15)
    ax = sns.countplot(data=data,x=feature,palette="Paired",order=data[feature].value_counts().index[:n].sort_values(),)

    for p in ax.patches:
        if perc == True:
            label = "{:.1f}%".format(100 * p.get_height() / total)
        else:
            label = p.get_height()

        x = p.get_x() + p.get_width() / 2
        y = p.get_height()
        ax.annotate(label,(x, y),ha="center",va="center",size=12,xytext=(0, 5),textcoords="offset points",)
    plt.show()