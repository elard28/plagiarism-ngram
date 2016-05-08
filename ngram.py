from __future__ import division

class NGram(set):
	def __init__(self, items=None, threshold=0.0, warp=1.0, key=None,
					N=3, pad_len=None, pad_char='$', **kwargs):
		super(NGram, self).__init__()
		if not (0 <= threshold <= 1):
			raise ValueError("threshold fuera de rango 0.0 to 1.0: "
							 + repr(threshold))
		if not (1.0 <= warp <= 3.0):
			raise ValueError(
				"warp fuera de rango 1.0 to 3.0: " + repr(warp))
		if not N >= 1:
			raise ValueError("N fuera de rango: " + repr(N))
		if pad_len is None:
			pad_len = N - 1
		if not (0 <= pad_len < N):
			raise ValueError("pad_len fuera de rango: " + repr(pad_len))
		if not len(pad_char) == 1:
			raise ValueError(
				"pad_char is not single character: " + repr(pad_char))
		if key is not None and not callable(key):
			raise ValueError("key no es funcion: " + repr(key))
		self.threshold = threshold
		self.warp = warp
		self.N = N
		self._pad_len = pad_len
		self._pad_char = pad_char
		self._padding = pad_char * pad_len  # derive a padding string
		# compatibility shim for 3.1 iconv parameter
		if 'iconv' in kwargs:
			self._key = kwargs.pop('iconv')
		# no longer support 3.1 qconv parameter
		if 'qconv' in kwargs:
			raise ValueError('sin soporte')
		self._key = key
		self._grams = {}
		self.length = {}
		if items:
			self.update(items)


	def add(self, item):
		if item not in self:
			super(NGram, self).add(item)
			padded_item = self.pad(self.key(item))
			self.length[item] = len(padded_item)
			for ngram in self._split(padded_item):
				self._grams.setdefault(ngram, {}).setdefault(item, 0)
				self._grams[ngram][item] += 1

	def remove(self, item):
		if item in self:
			super(NGram, self).remove(item)
			del self.length[item]
			for ngram in self.splititem(item):
				del self._grams[ngram][item]
	

	def items_sharing_ngrams(self, query):
		shared = {}
		remaining = {}
		for ngram in self.split(query):
			try:
				for match, count in self._grams[ngram].items():
					remaining.setdefault(ngram, {}).setdefault(match, count)
					# match as many occurrences as exist in matched string
					if remaining[ngram][match] > 0:
						remaining[ngram][match] -= 1
						shared.setdefault(match, 0)
						shared[match] += 1
			except KeyError:
				pass
		return shared

	@staticmethod
	def ngram_similarity(samegrams, allgrams, warp=1.0): 
		if abs(warp - 1.0) < 1e-9:
			similarity = float(samegrams) / allgrams
		else:
			diffgrams = float(allgrams - samegrams)
			similarity = ((allgrams ** warp - diffgrams ** warp)
					/ (allgrams ** warp))
		return similarity

	@staticmethod
	def compare(s1, s2, **kwargs):
		if s1 is None or s2 is None:
			if s1 == s2:
				return 1.0
			return 0.0
		try:
			return NGram([s1], **kwargs).search(s2)[0][1]
		except IndexError:
			return 0.0