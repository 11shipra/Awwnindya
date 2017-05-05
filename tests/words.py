import sys, os, string
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))
import numpy
import words

def randomtest(tests = 1000, lengths = 10, probability = .5):
	overlaplength, leftlength = int(probability * lengths), int(((1 - probability) * lengths) / 2.)
	oopscount, stringpool = 0, [numpy.random.choice([c for c in string.letters]) for _ in xrange(tests)]
	for _ in xrange(tests):
		randomstrings = [numpy.random.choice(stringpool) for __ in xrange(lengths)]
		strings = ' '.join(randomstrings)
		if words.smithwaterman(
			strings,
			' '.join(randomstrings[: overlaplength])
		) != overlaplength: oopscount += 1
		if words.smithwaterman(
			strings,
			' '.join(
				randomstrings[: overlaplength] +
				['*' for __ in xrange(lengths - overlaplength)]
			)
		) != overlaplength: oopscount += 1
		if words.smithwaterman(
			strings,
			' '.join(
				['*' for __ in xrange(lengths - overlaplength)] +
				randomstrings[: overlaplength]
			)
		) != overlaplength: oopscount += 1
		if words.smithwaterman(
			strings,
			' '.join(
				['*' for __ in xrange(leftlength)] +
				randomstrings[: overlaplength] +
				['*' for __ in xrange(lengths - overlaplength - leftlength)]
			)
		) != overlaplength: oopscount += 1
	return oopscount

def livetest(database, query):
	database = words.parse(database)
	maximum, matches = words.find(database, query)
	for index in matches:
		print database['timestamps'][index], database['texts'][index], database['speakers'][index]
