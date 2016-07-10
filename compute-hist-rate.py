# Compute the average exchange rate for CHF/USD.
#
# usage:
#   $> time python compute-hist-rate.py

import datetime
import ratewrapper

k_total_days = 360 * 5
k_days_to_stats = [7, 15, 30, 90, 180, 360, 360*2, 360*5]
k_hash_file = "rate.txt"


def calc_avg_std(xrate_map):
    ''' Compute average and middle value of the xrate array.
    '''
    n = len(xrate_map)
    avg = float(sum(xrate_map)) / n
    sq = sum((x-avg)**2 for x in xrate_map)
    # Divide by (n-1), from Bessel's correction.
    std = (sq/(n-1)) ** 0.5
    maxv = max(xrate_map)
    minv = min(xrate_map)
    midv = (maxv + minv) * 0.5
    # https://en.wikipedia.org/wiki/Standard_deviation#Rules_for_normally_distributed_data
    # 1 stdev, conf: 70%
    # 1.28 stddev, conf: 80%
    # 1.64 stddev, conf: 90%    
    print "Latest {0:4d} day(s), Mid: {3:.3f}, Avg: {1:.3f}, "\
        "[{4:.3f}, {5:.3f}]@70, StdDev: {2:.3f}"\
        .format(n, avg, std, midv, avg-std, avg+std)

def main():
    xrate_wrapper = ratewrapper.RateWrapper(k_hash_file)

    xrate_map = []
    today = datetime.date.today()
    for n in range(k_total_days):
        chf = xrate_wrapper.get_day_rate(today - datetime.timedelta(n))
        xrate_map.append(chf)

    for day in k_days_to_stats:
        if day > k_total_days:
            break
        calc_avg_std(xrate_map[:day])

if __name__ == "__main__":
    main()
