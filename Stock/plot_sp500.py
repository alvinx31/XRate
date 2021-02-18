import urllib.request as urlrq
import certifi
import ssl
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

TOP = 15  # The latest years to view.

def p2f(x):
    return float(x.strip('%'))/100

def fetch_data(url, top=30):
    print('Start fetching data table ...')
    resp = urlrq.urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))
    text = resp.read()
    soup = BeautifulSoup(text, 'html.parser')
    print('Finish fetching!')
    table = soup.find("table", { "id" : "datatable" })
    rows = table.findAll("tr")
    year = []
    val = []
    print('Collecting the data from table')
    for row in reversed(rows[2:top+1]):
        cells = row.findAll("td")
        date = cells[0].find(text=True).strip()
        value = cells[1].find(text=True).strip()
        year.append(int(date.split(',')[1]))
        val.append(value)
        # print(date, value)
    return year, val

url_t10y = 'https://www.multpl.com/10-year-treasury-rate/table/by-year'
url_sp500_pe = 'https://www.multpl.com/s-p-500-pe-ratio/table/by-year'

_, y_t10y = fetch_data(url_t10y, TOP)
x, y_sp500 = fetch_data(url_sp500_pe, TOP)
y = []
for i in range(len(y_t10y)):
    r_pe = 1.0 / float(y_sp500[i])
    rate = p2f(y_t10y[i])
    y.append((r_pe - rate) * 100.)

print('Ploting the graph ...')
ax = plt.axes()
ax.plot(x, y)
plt.show()
