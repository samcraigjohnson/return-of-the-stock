import urllib
import stock_list

base_url = "http://ichart.finance.yahoo.com/table.csv?s="
dest = "./old_data/"
file_nasdaq = "./setup/nas_stocks.txt"

#get csv of all prices of given symbol
def get_old_data(symb):
	url = base_url + symb
	file_name = dest + symb + '.csv'
	try:
		urllib.urlretrieve(url, file_name)

	except urllib.ContentTooShortError as e:
		outfile = open(file_name, "w")
		outfile.write(e.content)
		outfile.close()
	
	return file_name

#get every csv from yahoo of nasdaq
def get_all_data():
	stocks = stock_list.create_stock_list(file_nasdaq)
	for stock in stocks:
		get_old_data(stock['symbol'])

def get_adj_change(symb):
	lines = get_csv_data(symb)
	new_price = float(lines[1].split(',')[6])
	old_price = float(lines[2].split(',')[6])
	percent_change = (new_price-old_price)/(old_price)
	return percent_change

def get_close_change(symb):
	lines = get_csv_data(symb)
	new_price = float(lines[1].split(',')[4])
	old_price = float(lines[2].split(',')[4])
	percent_change = (new_price-old_price)/(old_price)
	return percent_change

def get_csv_data(symb):
	f_name = get_old_data(symb)
	csv = open(f_name, 'r')
	data = csv.read()
	lines = data.split('\n')
	csv.close()
	return lines