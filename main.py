from pcpartpicker import API
from csv import DictWriter
from pprint import pprint
from datetime import date
def to_dict(obj):
    """Recursively convert object to dict"""
    if hasattr(obj, '__dict__'):
        return {key: to_dict(val) for key, val in vars(obj).items()}
    elif isinstance(obj, (list, tuple)):
        return [to_dict(item) for item in obj]
    else:
        return obj

        

api = API("uk")
ram_data = api.retrieve("memory")["memory"]
ram_data = list(ram_data)


prices = []
lowest_price = float('inf')
highest_price = 0
for ram in ram_data:
    ram = to_dict(ram)
    if ram['module_type'] == 'DDR4':# i want to find the cheapest and most expensive and list the name of the product.
        ram_price = ram['price_per_gb']['amount']
        if ram_price<lowest_price and ram_price > 0:
            cheap_ram = ram
            lowest_price = ram_price
        if ram_price > highest_price:
            expensive_ram = ram
            highest_price = ram_price

        prices.append(ram_price)

average_ram_price = sum(prices) / len(prices)
lowest_price = round(lowest_price, 2)
highest_price = round(highest_price, 2)
average_ram_price = round(average_ram_price, 2)

new_row = {
    'date' : date.isoformat(date.today()),
    'average_price_per_gb' : average_ram_price,
    'most_expensive_ram' : f'{expensive_ram['brand']}|{expensive_ram['model']}|£{highest_price}',
    'least_expensive_ram' : f'{cheap_ram['brand']}|{cheap_ram['model']}|£{lowest_price}'
}
fields = new_row.keys()

with open(file='ram_prices.csv', mode='a') as file:
    writer = DictWriter(file, fields)
    writer.writerow(new_row)
