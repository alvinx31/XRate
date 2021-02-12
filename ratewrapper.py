import json
import urllib2

access_key='8886438d5dcb063d80a10feb133f884c'

_DEBUG = False

class RateWrapper:
    ''' Store historical exchange rate data light weight locally, 
    and provide an access API by day searching, to reduce unnecessary 
    http request.

    And the local database will update accordingly after using.
    '''

    def __load_hash(self):
        self.__xrate_hash = {}
        try:
            with open(self.__hash_file, "r") as f:
                for line in f:
                    k, v = line.split(',')
                    self.__xrate_hash[k] = float(v)
        except IOError:
            pass

    def __dump_hash(self):
        with open(self.__hash_file, "w") as f:
            for k, v in self.__xrate_hash.iteritems():
                f.write("{},{}\n".format(k, v))

    def __get_hash_key(self, day):
        return "{:%Y-%m-%d}".format(day)

    def generate_url(self, day):
        ''' Generate the http request url to fetch the json data for given day.

        Get historical rates for any day since 1999 from
        http://api.fixer.io/2000-01-03?base=USD.
        '''
        url = "http://data.fixer.io/api/{:%Y-%m-%d}?access_key={}".format(day, access_key)
        if _DEBUG:
            print url
        return url

    def get_day_rate(self, day):
        k = self.__get_hash_key(day)
        if self.__xrate_hash.has_key(k):
            return self.__xrate_hash[k]
        try:
            day_rate = json.loads(urllib2.urlopen(self.generate_url(day), timeout=1).read())
            if _DEBUG:
                print day_rate
        except:
            day_rate = json.loads(urllib2.urlopen(self.generate_url(day), timeout=5).read())

        # Exclude days which the market is unavailable, i.e. holidays.
        if k == day_rate['date']:
            self.__xrate_hash[k] = day_rate['rates']['CHF'] / day_rate['rates']['USD']
            return self.__xrate_hash[k]
        return -1

    def __init__(self, hash_file):
        self.__hash_file = hash_file
        self.__load_hash()

    def __del__(self):
        self.__dump_hash()
