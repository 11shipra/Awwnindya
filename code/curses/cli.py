import sys, os, curses, time, string, textwrap
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import words

def maxlength(dictoflists, keys):
	return [max([len(alist) for alist in dictoflists[key]]) for key in keys]

database, cursor, conversation = words.parse(sys.argv[1]), -1, list()
widthp1, widthp2, widthp3 = maxlength(database, ['timestamps', 'speakers', 'texts'])
heading, tailing, paddingx, paddingy, widthp4, heightp5, widthp = 3, 1, 1, 1, 30, 1, 2

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
stdscr.refresh()

height, width = stdscr.getmaxyx()
heightl, heightp4 = len(database['texts']), height - heightp5 - heading - 4 * paddingy

stdscr.addstr(1, 1, 'Awwnindya', curses.A_BOLD)
stdscr.addstr(2, 1, '%s : %s' %(database['speakers'][0], database['speakers'][1]), curses.A_REVERSE)
timestamps = curses.newpad(heightl, widthp1 + 1)
speakers = curses.newpad(heightl, widthp2 + 1)
texts = curses.newpad(heightl, widthp3 + 1)
dialogues = curses.newpad(height, widthp4 + 1)
inputs = curses.newpad(heightp5, width - widthp - 3 * paddingx + 1)

timestamps.addstr(0, 0, '\n'.join(database['timestamps']))
speakers.addstr(0, 0, '\n'.join(database['speakers']))
texts.addstr(0, 0, '\n'.join(database['texts']))
dialogues.addstr(0, 0, 'type and hit enter to search')
dialogues.addstr(1, 0, 'use the arrow keys to navigate')
dialogues.addstr(2, 0, 'hit end to quit')

stdscr.addstr(height - heightp5 - paddingy, 0, ' >')

x, y, ix = 0, 0, 0
while True:
	timestamps.refresh(
		y, 0,
		heading + paddingy, paddingx,
		height - heightp5 - 3 * paddingy, paddingx + widthp1
	)
	speakers.refresh(
		y, 0,
		heading + paddingy, 3 * paddingx + widthp1,
		height - heightp5 - 3 * paddingy, 3 * paddingx + widthp1 + widthp2
	)
	texts.refresh(
		y, x,
		heading + paddingy, 5 * paddingx + widthp1 + widthp2,
		height - heightp5 - 3 * paddingy, width - 3 * paddingx - widthp4 - 1 #
	)
	dialogues.refresh(
		0, 0,
		heading + paddingy, width - paddingx - widthp4,
		height - heightp5 - 3 * paddingy, width - paddingx
	)
	inputs.refresh(
		0, 0,
		height - heightp5 - paddingy, widthp + 2 * paddingx,
		height, width - paddingx
	)

	c = stdscr.getch()
	if c == curses.KEY_END: break
	elif c == curses.KEY_UP: y -= 1
	elif c == curses.KEY_LEFT: x -= 1
	elif c == curses.KEY_DOWN: y += 1
	elif c == curses.KEY_RIGHT: x += 1
	elif c == curses.KEY_BACKSPACE:
		ix -= 1
		if ix >= 0: inputs.delch(0, ix)
	elif c == curses.KEY_ENTER or c == ord('\n') or c == ord('\r'):
		istring = inputs.instr(0, 0)
		cursor = words.next(database, istring.strip(), cursor)
		ostring = database['texts'][cursor]
		conversation.extend(
			textwrap.wrap('>> ' + istring, widthp4) + ['\n'] + 
			textwrap.wrap('<< ' + ostring, widthp4) + ['\n']
		)
		conversation = conversation[-heightp4: ]
		dialogues.erase()
		for iy in xrange(len(conversation)):
			dialogues.addstr(iy, 0, conversation[iy])
		y = cursor
		inputs.erase()
		ix = 0
	elif c in [ord(char) for char in string.printable]:
		if ix < width - widthp - 3 * paddingx: inputs.addch(0, ix, c)
		ix += 1
	x, y = min(max(0, x), widthp3), min(max(0, y), heightl)
	ix = min(max(0, ix), width - widthp - 3 * paddingx)

curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
