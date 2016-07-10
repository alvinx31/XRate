class RateWrapper:
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
			for k, v in __xrate_hash.iteritems():
				f.write("{},{}\n".format(k,v))			

	def __get_hash_key(self, day):
		return "{:%Y-%m-%d}".format(day)

	def get_day_rate(self, day):
		k = self.__get_hash_key(day)
		if self.__xrate_hash.has_key(k):
			return self.__xrate_hash[k]		
		day_rate = json.loads(urllib2.urlopen(generate_url(day)).read())
		self.__xrate_hash[k] = day_rate['rates']['CHF']
		return day_rate['rates']['CHF']

	def __init__(self, hash_file):
		self.__hash_file = hash_file
		self.__load_hash()

	def __exit__(self, exc_type, exc_value, traceback):
	    self.__dump_hash()