import re

pattern = re.compile('^(\d\d)/(\d\d)/(\d\d\d\d), (\d\d):(\d\d) - ([\w ]*):(.*)$')
words = lambda string: map(
    lambda word: word.lower(),
    filter(lambda char: char.isalpha() or char.isspace(), string.strip()).split()
)
similarity = lambda char1, char2: 1 if char1.lower() == char2.lower() else -1

def parse(filename):
	database, lastspeaker = {'timestamps': list(), 'texts': list(), 'speakers': list()}, None
	for line in open(filename):
		matches = pattern.match(line.strip())
		if not matches: database['texts'][-1] += ' ' + line.strip()
		else:
			groups = matches.groups()
			if lastspeaker == groups[5]: database['texts'][-1] += ' %s' %groups[6].strip()
			else:
				database['timestamps'].append(
					'%s:%s:%s:%s:%s'
					%(groups[2], groups[1], groups[0], groups[3], groups[4])
				)
				database['speakers'].append(groups[5])
				database['texts'].append(groups[6].strip())
				lastspeaker = groups[5]
	return database

def smithwaterman(string1, string2):
	string1, string2 = words(string1), words(string2)
        table = [[0 for ii in xrange(len(string2) + 1)] for i in xrange(len(string1) + 1)]
	for i in xrange(len(string1)):
		for ii in xrange(len(string2)):
			table[i + 1][ii + 1] = max(
				0,
				table[i][ii + 1] - 1,
				table[i + 1][ii] - 1,
				table[i][ii] + similarity(string1[i], string2[ii])
			)
	return max(table[i][ii] for i in xrange(len(string1) + 1) for ii in xrange(len(string2) + 1))

def find(database, query):
	maximum, matches = -1, list()
	for i in xrange(len(database['texts'])):
		match = smithwaterman(database['texts'][i], query)
		if maximum < match: maximum, matches = match, [i]
		elif maximum == match: matches.append(i)
	return maximum, matches
