# Compute the average exchange rate for CHF/USD.
#
# usage:
#   $> time python compute-hist-rate.py

import datetime
import urllib2
import json
import ratewrapper

k_total_days = 360
days_to_stats = [7, 15, 30, 60, 90, 180, 360]
hash_file = "rate.txt"

# Get historical rates for any day since 1999.
# http://api.fixer.io/2000-01-03?base=USD
def generate_url(day):
	return "http://api.fixer.io/{:%Y-%m-%d}?base=USD".format(day)

def calc_avg_std(xrate_map, n):
	avg = float(sum(xrate_map)) / n
	sq = sum((x-avg)**2 for x in xrate_map)
	# Divide by (n-1), from Bessel's correction.
	std = (sq/(n-1)) ** 0.5
	maxv = max(xrate_map)
	minv = min(xrate_map)
	midv = (maxv + minv) * 0.5
	print "Latest {0:} day(s), Mid: {3:.3f}, Avg: {1:.3f}, "\
	  "StdDev: {2:.3f}".format(n, avg, std, midv)

def main():
	xrate_wrapper = ratewrapper.RateWrapper(hash_file)
	
	xrate_map = []
	today = datetime.date.today()
	for n in range(k_total_days):
		chf = xrate_wrapper.get_day_rate(today - datetime.timedelta(n))
		xrate_map.append(chf);

	for day in days_to_stats:
		if day > k_total_days:
			break
		calc_avg_std(xrate_map[:day], day)

if __name__ == "__main__":
	main()