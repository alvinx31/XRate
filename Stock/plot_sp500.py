import urllib.request as urlrq
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

import time
import datetime
import matplotlib.dates as mdates
import numpy as np
from matplotlib.pyplot import MultipleLocator

TOP = 300  # The latest months to view.
url_t10y = 'https://www.multpl.com/10-year-treasury-rate/table/by-month'
url_sp500_pe = 'https://www.multpl.com/s-p-500-pe-ratio/table/by-month'

def p2f(x):
    return float(x.strip('%'))/100

def dfs_urlopen(url, timeout=1):
    try:
        resp = urlrq.urlopen(url, timeout=timeout)
    except:
        return dfs_urlopen(url, timeout * 2)
    return resp

def fetch_data(url, top=30):
    print('Start fetching data table ...')
    resp = dfs_urlopen(url)
    text = resp.read()
    soup = BeautifulSoup(text, 'html.parser')
    print('Finish fetching!')
    table = soup.find("table", { "id" : "datatable" })
    rows = table.findAll("tr")
    year = []
    val = []
    print('Collecting the data from table')

    for row in reversed(rows[1:top+1]):
        cells = row.findAll("td")
        curdate = cells[0].find(text=True).strip()
        value = cells[1].find(text=True).strip()

        # date format: Jan 1, 2021
        curdate = time.strptime(curdate, '%b %d, %Y')
        curdate = datetime.date.fromtimestamp(time.mktime(curdate))
        year.append(curdate)
        val.append(value)
    return year, val


_, y_t10y = fetch_data(url_t10y, TOP)
x, y_sp500 = fetch_data(url_sp500_pe, TOP)
y = []
for i in range(len(y_t10y)):
    r_pe = 1.0 / float(y_sp500[i])
    rate = p2f(y_t10y[i])
    y.append((r_pe - rate) * 100.)

print('Ploting the graph ...')

ax = plt.axes()
# round to nearest years...
datemin = np.datetime64(x[0], 'Y')
datemax = np.datetime64(x[-1], 'Y') + np.timedelta64(1, 'Y')
ax.set_xlim(datemin, datemax)

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')
# format the ticks
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)

y_major_locator=MultipleLocator(1)
y_minor_locator=MultipleLocator(0.2)
ax.yaxis.set_major_locator(y_major_locator)
ax.yaxis.set_minor_locator(y_minor_locator)

ax.plot(x, y, label = 'Premium return over risk (as %)')
ax.plot(x, [0]*len(x), linestyle='dashed', label = 'Base line')
plt.legend()
plt.show()
