import datetime
import urllib2
import json

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
	print "Latest {0:} day(s), Mid: {3:.3f}, Avg: {1:.3f}, StdDev: {2:.3f}".format(n, avg, std, midv)

def load_hash():	
	xrate_hash = {}
	try:
		with open(hash_file, "r") as f:
			for line in f:
				k, v = line.split(',')
				xrate_hash[k] = float(v)
	except IOError:
		pass
	return xrate_hash

def dump_hash(xrate_hash):
	with open(hash_file, "w") as f:
		for k, v in xrate_hash.iteritems():
			f.write("{},{}\n".format(k,v))			

def get_hash_key(day):
	return "{:%Y-%m-%d}".format(day)

def get_day_rate(day, xrate_hash):
	k = get_hash_key(day)
	if xrate_hash.has_key(k):
		return xrate_hash[k]		
	day_rate = json.loads(urllib2.urlopen(generate_url(day)).read())
	xrate_hash[k] = day_rate['rates']['CHF']
	return day_rate['rates']['CHF']

def main():
	today = datetime.date.today()
	xrate_hash = load_hash()
	xrate_map = []

	for n in range(k_total_days):
		day = today - datetime.timedelta(n)
		chf = get_day_rate(day, xrate_hash)
		xrate_map.append(chf);

	for day in days_to_stats:
		if day > k_total_days:
			break
		calc_avg_std(xrate_map[:day], day)
	
	dump_hash(xrate_hash)

if __name__ == "__main__":
	main()