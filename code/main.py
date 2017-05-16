import os, random
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.image import Image

import words

class SubScreen(BoxLayout):
	def __init__(self, **kwargs):
		super(SubScreen, self).__init__(**kwargs)

		self.database, self.cursor, self.lines = words.parse(os.path.join(path, 'database.txt')), -1, list()
		self.imageid = random.choice([os.path.join(path, filename) for filename in os.listdir(path) if os.path.isfile(os.path.join(path, filename))])
		
		self.orientation = 'vertical'
		self.inputtext = TextInput(multiline = False)
		self.add_widget(self.inputtext)
		self.button = Button(text = 'Awwnindya', font_size = 14, on_press = self.update)
		self.add_widget(self.button)
		self.image = kwargs['image']
		self.image.source = self.imageid
		self.image.reload()

	def update(self, event):
		inputtext = ' '.join(words.words(self.inputtext.text.strip())).strip()
		self.cursor = words.next(self.database, inputtext, self.cursor) % len(self.database)
		self.lines = self.lines[-9: ] + [inputtext, ' '.join(words.words(self.database['texts'][self.cursor])).strip()]
		self.button.text = '\n'.join(self.lines)

		self.imageid = random.choice([os.path.join(path, filename) for filename in os.listdir(path) if os.path.isfile(os.path.join(path, filename))])
		self.image.source = self.imageid
		self.image.reload()

class Screen(GridLayout):
	def __init__(self, **kwargs):
		super(Screen, self).__init__(**kwargs)
		self.rows, self.columns = 1, 2
		self.image = Image()
		self.add_widget(self.image)
		self.text = SubScreen(image = self.image)
		self.add_widget(self.text)

class Awwnindya(App):
	def build(self):
		return Screen()

if __name__ == '__main__':
	Awwnindya().run()
