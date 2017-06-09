import sys, os, textwrap
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import words

class Screen(BoxLayout):
	def __init__(self, **kwargs):
		super(Screen, self).__init__(**kwargs)
		self.orientation = 'vertical'
		self.database, self.cursor, self.lines = words.parse(os.path.join(path, 'database.txt')), -1, list()
		self.label = Label(text = 'Awwnindya', font_size = 14, size_hint = (1., .9))
		self.add_widget(self.label)
		self.inputtext = TextInput(multiline = False, size_hint = (1., .1))
		self.inputtext.bind(on_text_validate = self.remember)
		self.add_widget(self.inputtext)

	def remember(self, event):
		inputtext = ' '.join(words.words(self.inputtext.text.strip())).strip()
		self.cursor = words.next(self.database, inputtext, self.cursor) % len(self.database['texts'])
		self.lines = self.lines[-9: ] + ['>> ' + inputtext, '<< ' + '\n'.join(textwrap.wrap(' '.join(words.words(self.database['texts'][self.cursor])).strip()))]
		self.label.text = '\n'.join(self.lines)

class Awwnindya(App):
	def build(self):
		return Screen()

if __name__ == '__main__':
	Awwnindya().run()
