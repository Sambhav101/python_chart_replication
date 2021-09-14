import csv
import collections
from flask import Flask, render_template


app = Flask(__name__)

data = []
with open('data.csv') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        data.append(row)

# clean the data 
def clean_data(data):
    for row in data:
        if row['website'] == 'vod':
            row['website'] = 'Vodafone'
        elif row['website'] == 'tel':
            row['website'] = 'Telekom'
            
    return data


# return headers of data
def get_headers(data):
    tariff_mbit = []
    for row in data:
        tariff_mbit.append((row['website'], row['download_speed']))
    
    count = collections.Counter(tariff_mbit)
    header = {}
    for k, v in count.items():
        if k[0] in header: 
            if header[k[0]] < v:
                header[k[0]] = v
        else:
            header[k[0]] = v
    
    header_items = []
    for item in header:
        for times in range(header[item]):
            header_items.append(item)
    
    return header_items


# ge4t the row fo data
def get_rows(data):
    d_speeds = []
    for row in data:
        if int(row['download_speed']) not in d_speeds:
            d_speeds.append(int(row['download_speed']))
    return sorted(d_speeds)


# wrap item s in li tag
def wrap_li(items):
    li_items=""
    for item in items:
        li_items += '<li>'+ str(item) + '</li>'
    return '<ul style="list-style: none;">' + li_items + '</ul>'


# return all the data based on mbits and headers
def get_data(data, headers, mbit):
    res = [0] * len(headers)
    print(res)
    for row in data:
        if row['download_speed'] == str(mbit):
            index = headers.index(row['website'])
            while res[index] != 0:
                index += 1
            res[index] = row
    
    return res


@app.route('/')
def index():

	return render_template('index.html', headers = headers, rows = rows, data = data, get_data = get_data)


if __name__ == '__main__':
	data = clean_data(data)
	headers = get_headers(data)
	rows = get_rows(data)
	app.run(debug=True)
