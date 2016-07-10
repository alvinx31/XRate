import json
import urllib2


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
        return "http://api.fixer.io/{:%Y-%m-%d}?base=USD".format(day)

    def get_day_rate(self, day):
        k = self.__get_hash_key(day)
        if self.__xrate_hash.has_key(k):
            return self.__xrate_hash[k]
        day_rate = json.loads(urllib2.urlopen(self.generate_url(day)).read())

        # Exclude days which the market is unavailable, i.e. holidays.
        if k == day_rate['date']:
            self.__xrate_hash[k] = day_rate['rates']['CHF']
            return day_rate['rates']['CHF']
        return -1

    def __init__(self, hash_file):
        self.__hash_file = hash_file
        self.__load_hash()

    def __del__(self):
        self.__dump_hash()
