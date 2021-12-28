class BoyerMooreHorspool:
	def __init__(self, text, pattern):
		self.text = text
		self.pattern = pattern
		self.m = len(pattern)
		self.n = len(text)
		self.skip = []
		for i in range(256): self.skip.append(-1)
		for i in range(self.m): self.skip[ord(pattern[i])] = self.m

	def search(self):
		for i in range(self.n + self.m + 1):
			skip = 0
			for j in range(self.m-1, -1, -1):
				if self.text[i+j] != self.pattern[j]:
					skip = j - self.skip[ord(self.text[i+j])]
					if skip < 1: skip = 1
					break

			if skip == 0:
				print("Found at {0}".format(i))
				return

			i += skip

		print("Not Found")
		return

#file = BoyerMooreHorspool("dnabwefabcdnew","abcd")
#file.search()
