import urllib.request as urlrq
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

import time
import datetime
import matplotlib.dates as mdates
import numpy as np
from matplotlib.pyplot import MultipleLocator

TOP = 25 * 12  # The latest months to view.
url_t10y = 'https://www.multpl.com/5-year-treasury-rate/table/by-month'
url_sp500_pe = 'https://www.multpl.com/s-p-500-pe-ratio/table/by-month'
url_sp500_dividend = 'https://www.multpl.com/s-p-500-dividend-yield/table/by-month'

def p2f(x):
    return float(x.strip('%'))/100

def dfs_urlopen(url, timeout=1):
    try:
        resp = urlrq.urlopen(url, timeout=timeout)
    except:
        return dfs_urlopen(url, timeout * 2)
    return resp

def fetch_data(url, top=120):
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

msg = 'Select the mode to analysis\n  0): The Simple\n  1): The Comprehensive\n'
mode_comp = input(msg) == '1'

_, y_t10y = fetch_data(url_t10y, TOP)
x, y_sp500 = fetch_data(url_sp500_pe, TOP)
if mode_comp:
    _, y_div = fetch_data(url_sp500_dividend, TOP)
y = []
y2 = []
for i in range(len(y_t10y)):
    r_pe = 1.0 / float(y_sp500[i])
    rate = p2f(y_t10y[i])
    ret = (r_pe - rate) * 100.
    if mode_comp:
        ret = ret + p2f(y_div[i]) * 100.
    y.append(ret)
    y2.append(rate * 100.)

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

miny = round(min(np.min(y), np.min(y2)) - 0.5)
maxy = round(max(np.max(y), np.max(y2)) + 0.5)
ax.set_ylim(miny, maxy)

# show y-axis in the right side.
ax2 = ax.twinx()
ax2.set_ylim(miny, maxy)
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
# ax2.grid(None)

ax.plot(x, y, label = 'S&P 500 Equity Risk Premium (as %)')
ax.plot(x, y2, label = '5 Year Treasury Rate (as %)')
ax.legend()
ax.grid()
plt.show()
