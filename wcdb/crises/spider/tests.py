import unittest

from spider import *

class TestSpider(unittest.TestCase):

	def test_ensureTrailingSlash1(self):
		self.assertEqual(ensureTrailingSlash(""), "")
		self.assertEqual(ensureTrailingSlash("   "), "")

	def test_ensureTrailingSlash2(self):
		self.assertEqual(ensureTrailingSlash("abcd"), "abcd/")
		self.assertEqual(
			ensureTrailingSlash("http://tcp-connections.herokuapp.com/organizations/1"), 
			"http://tcp-connections.herokuapp.com/organizations/1/")

	def test_ensureTrailingSlash3(self):
		self.assertEqual(ensureTrailingSlash("abcd/"), "abcd/")
		self.assertEqual(ensureTrailingSlash("/"), "/")
		self.assertEqual(ensureTrailingSlash("//"), "//")

	def test_trimTrailingSlashes1(self):
		self.assertEqual(trimTrailingSlashes(""), "")
		self.assertEqual(trimTrailingSlashes("    "), "")

	def test_trimTrailingSlashes2(self):
		self.assertEqual(trimTrailingSlashes("abcd/"), "abcd")
		self.assertEqual(trimTrailingSlashes("abcd//"), "abcd")
		self.assertEqual(trimTrailingSlashes("abcd///////"), "abcd")
		self.assertEqual(
			trimTrailingSlashes("http://tcp-connections.herokuapp.com/organizations/1/"), 
			"http://tcp-connections.herokuapp.com/organizations/1")

	def test_trimTrailingSlashes3(self):
		self.assertEqual(trimTrailingSlashes("abcd"), "abcd")
		self.assertEqual(trimTrailingSlashes("/"), "")
		self.assertEqual(trimTrailingSlashes("  /  "), "")

	def test_joinUrls1(self):
		bases = ["http://tcp-connections.herokuapp.com/", "http://tcp-connections.herokuapp.com"]
		rels = ["/crises", "crises"]
		for base in bases:
			for rel in rels:
				self.assertEqual(joinUrls(base, rel), "http://tcp-connections.herokuapp.com/crises")

	def test_joinUrls2(self):
		base = "http://tcp-connections.herokuapp.com/crises"
		rel1 = "1"
		self.assertEqual(joinUrls(base, rel1), "http://tcp-connections.herokuapp.com/crises/1")
		# this is a tricky case to watch out for
		rel2 = "/1"
		self.assertEqual(joinUrls(base, rel2), "http://tcp-connections.herokuapp.com/1")

	def test_joinUrls3(self): 
		base = "http://tcp-connections.herokuapp.com/"
		rel = "http://en.wikipedia.com"
		self.assertEqual(joinUrls(base, rel), rel)
		self.assertEqual(joinUrls(rel, base), base)

	def test_joinUrls4(self):
		bases = ["http://tcp-connections.herokuapp.com/", "http://tcp-connections.herokuapp.com/crises"]
		rels = ["http://tcp-connections.herokuapp.com/people", "/people"]
		for base in bases:
			for rel in rels:
				self.assertEqual(joinUrls(base, rel), "http://tcp-connections.herokuapp.com/people")

	def test_wordsFromText1(self):
		text = "   something   1234 \t \n \r \x0d SOMETHINGELSE"
		self.assertEqual(wordsFromText(text), ["something", "1234", "somethingelse"])

	def test_wordsFromText2(self):
		text = "\x80\x81\x8f\x90\x99\x9a\x9f"
		self.assertEqual(wordsFromText(text), [])

	def test_wordsFromText3(self):
		text = "(FBI)@#$@%.,-\x901960s"
		self.assertEqual(wordsFromText(text), ["fbi", "1960s"])


if __name__ == '__main__':
	unittest.main()
