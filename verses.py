'''
Title: 
Bible Verse Parser


Description:
tkinter from to take openbible.info verses and dump to topically sorted csv

I like to study the Bible by topic and then dig deeper when I want to know context.

We've been told that the only weapon we have in spiritual warfare is the word of God
I often try to memorize these using "jmemorize".  This program helps me format
my data for jmemorize

Also This Script teaches:
tkinter basics
tkinter grid layout
tkinter buttons, fields
tkinter form field error checking
tkinter popups
regex/find
classes
basic flow control in loops
splits/joins
dictionaries
opening browser


Error checking is very basic and really just sees if there is ANY data
It's counting on the regex/find finding things and if not, it failed



'''

import tkinter as tk
import tkinter.messagebox as mb
import json
import re
import webbrowser

# can probably not do this, but am testing still:
from tkinter import *
from tkinter.ttk import *

# general appearances
opts1 = { 'ipadx': 5, 'ipady': 5 , 'sticky': 'nswe' } # centered and stretched
opts2 = { 'ipadx': 0, 'ipady': 5 , 'sticky': 'ew' } # stick to both east & west side stretched
# -column, -columnspan, -in, -ipadx, -ipady, -padx, -pady, -row, -rowspan, or -sticky

bgcolor = '#ECECEC'
white = '#FFFFFF'
red = '#FF0000'

class Verses(tk.Tk):
	def __init__(self):
		super().__init__()

		# surely there is a better way to select on click
		# basically I had to define it first (probaly as I don't understand classes)
		# then when they click on the text area it auto selects all
		def select_all(event):
			self.text.tag_add("sel", "1.0", "end") # this is the only version of SEL or "sel", etc that worked
			self.text.focus_set()	# weird glitch requires focus after selecting to display the selection
			return 'break'			# another oddity in how the mainloop process works

		# predefine variables we are using/looking for
		self.b = tk.StringVar()
		self.c = tk.StringVar()
		self.t = tk.StringVar()

		# the title bar
		self.title("openbible.info Parser Helper")

		# corners for spacing/layout
		# I wanted equal spacing on both sides of my grid layout objects
		# the solution was a space as a label todo: what is better way?
		self.label_nw = tk.Label(self, text=" ", bg=bgcolor)
		self.label_nw.grid(row=0, column=0, **opts1)
		self.label_ne = tk.Label(self, text=" ", bg=bgcolor)
		self.label_ne.grid(row=0, column=9, **opts1)

		# first header
		self.label_a = tk.Label(self, text="Paste Verse Info Below", bg=bgcolor)
		self.label_a.grid(row=0, column=1, columnspan=8, **opts1)
		
		# the input text block
		self.text = tk.Text(self, width=60, height=5, bg=white)

		# text box placed after defined
		self.text.grid(row=1, column=1, columnspan=8, rowspan=5, **opts1)
		self.text.bind('<FocusIn>', select_all)
		self.text.bind('<Double-Button-1>', select_all)
		#self.text.bind('<Activate>', select_all)

		# second header/blank
		self.label_b = tk.Label(self, text="Click Parse, then Export:", bg=bgcolor)
		self.label_b.grid(row=8, column=1, columnspan=8, **opts1)

		# buttons
		self.btn_search = tk.Button(self, text="Search",command=self.search_topic, bg=bgcolor)
		self.btn_search.grid(row=9,column=1, columnspan=2, **opts1)
		#self.btn_search.focus_set() # works, but decided I didn't want it to work

		self.btn_parse = tk.Button(self, text="Parse",command=self.parse_only, bg=bgcolor)
		self.btn_parse.grid(row=9,column=3, columnspan=2, **opts1)

		self.btn_parse2 = tk.Button(self, text="Export",command=self.parse_export, bg=bgcolor)
		self.btn_parse2.grid(row=9,column=5, columnspan=2, **opts1)

		self.btn_clear = tk.Button(self, text="Sample",command=self.clear_text, bg=bgcolor)
		self.btn_clear.grid(row=9, column=7, columnspan=2, **opts1)

		# second header
		self.label_c = tk.Label(self, text="Parsed Output:", bg=bgcolor)
		self.label_c.grid(row=10, column=1, columnspan=8, **opts1)
		
		# manual form
		tk.Label(self, text="Book:").grid(row=11, column=1, columnspan=1, **opts2)
		tk.Entry(self, textvariable=self.b, width=15).grid(row=11, column=2, columnspan=2, **opts2)

		tk.Label(self, text="Topic:").grid(row=11, column=4, columnspan=1, **opts2)
		tk.Entry(self, textvariable=self.c, width=15).grid(row=11, column=5, columnspan=4, **opts2)
		#self.c.bind('<Return>', search_topics) # couldn't get this to work as planned

		tk.Label(self, text="Text:").grid(row=12, column=1, columnspan=1, **opts2)
		tk.Entry(self, textvariable=self.t, width=40).grid(row=12, column=2, columnspan=7, **opts2)

		# final header
		self.label_d = tk.Label(self, text=" ", bg=bgcolor)
		self.label_d.grid(row=13, column=1, columnspan=8, **opts1)

		# give basic instructions to user
		#mb.showinfo("Information", "1. Search a Topic\n2. Cut and Paste the verse+text\n3. Click Parse or Export\n4. Review your spreadsheet later using jmemorize")
		#return
		#self.c.focus_set() # no work, totally screws up the frame/focus requiring 
		# you to click off then on to get focus back.

	def search_topic(self):
		topic = self.c.get()		# get the data
		' '.join(topic.strip())		# strip and rebuilt with only useful whitespace
		topic.replace(" ", "_")     # replace spaces with underscores

		if (len(topic) < 3):
			mb.showinfo("Information", "No topic.  Please search after you type a valid topic")
		else:
			# build URL
			url = 'https://www.openbible.info/topics/' + topic
			# then open it in new tab of default browser
			webbrowser.open(url, new = 2)

	def clear_text(self):
		# clear out the trash and give us sample data for testing
		# probably not useful for anyone after they see how program works
		# I used it 
		self.text.delete("1.0", tk.END)
		self.b.set("")
		self.t.set("")

		# load sample data
		sample = "\nJames 4:6 ESV / 30 helpful votes\nBut he gives more grace. Therefore it says, “God opposes the proud, but gives grace to the humble.”\n"
		self.text.insert(tk.INSERT, sample)
		print("Sample data loaded")

	def parse_only(self):
	# parses big block and fills out fields with data we wanted 
	# added this to verify data before parsing into CSV permanently
	# not really useful now that wee have looked at data thoroughly, probably

		# text widget adds a new line, so check if right before that there is nothing
		# couldn't get this to work either.  todo
		if len(self.text.get("1.0", "end-1c")) == 0:
			mb.showinfo("Information", "No Data to Parse.  Click 'Sample' for Sample Data")
		else:
			# load up our data
			data = self.text.get("1.0", tk.END)
			lines = data.split("\n")

			# skip through weird sometimes blank lines and only load real data
			iter = 0
			for line in lines:
				if (len(line) < 2):
					iter = iter + 1
					continue
				else:
					break

			# ok we think this is the right stuff
			bcv = lines[iter]
			texts = lines[iter + 1]

			# regex wasn't necessary and overcomplicated stuff, use find()
			bcv = bcv[0:bcv.find(' ESV')]

			# we parsed it out above, so 
			self.b.set(bcv)
			if (len(texts) < 3):
				mb.showinfo("Information", "Your Book, Chapter, Verse seems very very short.  Verify it")
			
			# don't put that weird stuff in my flashcards!
			texts = re.sub(u'[\u201c\u201d]','"',texts) # ” and “ pet peeves

			# ok, it's clean (enough), so display it.
			self.t.set(texts)
			if (len(texts) < 3):
				mb.showinfo("Information", "The actual scripture seems very very short.  Verify it")

	def print_selection(self):
	# dumps selection under mouse, or defaults to form fields  to screen
	# put in place for error checking, not really needed for any function
	# kept for demonstration purposes
		selection = self.text.tag_ranges(tk.SEL)

		# IF you have something selected
		if selection:
			content = self.text.get(*selection)
			print(content)
		# ELSE just print the parse
		else:
			content = self.c.get() + "|" + self.b.get() + "|" + self.t.get() + "\n"
			print(content)

	def parse_export(self):
	# dumps captured data to csv file

		# text widget adds a new line, so check if right before that there is nothing
		# couldn't get this to work either.  todo
		if len(self.text.get("1.0", "end-1c")) == 0:
			mb.showinfo("Information", "No Data to Parse.  Click 'Clear' for Sample Data")
		else:
			# load up our data
			data = self.text.get("1.0", tk.END)
			lines = data.split("\n")

			# skip through weird sometimes blank lines
			iter = 0
			for line in lines:
				if (len(line) < 2):
					iter = iter + 1
					continue
				else:
					break

			# ok we think lines[] is the right stuff, get the raw
			bcv = lines[iter]
			texts = lines[iter + 1]

			# regex wasn't necessary and overcomplicated stuff
			# however, this will break if the input data differs
			bcv = bcv[0:bcv.find(' ESV')]

			# topic is manually typed in and can be anything
			topic = self.c.get()

			# clean ups would be better in a separate function I tink: todo
			bcv = re.sub('[\|]',"", bcv, 100) # rip out the pipes
			topic = re.sub('[\|]',"", topic, 100)
			text = re.sub('[\|]',"", texts, 100)
			textb = re.sub(u'[\u201c\u201d]','"',text, 100) # ” and “ pet peeve

			# we parsed it out above, so it's clean enough to redisplay the cleaned version
			self.b.set(bcv)
			self.t.set(textb)

			# basic error checking, better to make function: todo
			flag = 1
			if (len(bcv) < 3):
				mb.showinfo("Information", "Book Field Empty?")
				flag = 0

			if (len(textb) < 3):
				mb.showinfo("Information", "Text Field Empty?")
				flag = 0

			if (len(topic) < 3):
				mb.showinfo("Information", "Topic Field Empty?")
				flag = 0

			# error checking done, do the work
			if (flag):
				# This is our dump file
				file = 'verses.csv'

				# write to file, append mode
				with open(file, 'a') as outfile:
					outfile.write(topic + "|" + bcv + "|" + textb + "\n")

				# explain to user what happened
				print(file + " updated: " + topic + "|" + bcv)
			else:
				# or don't do anything and let them know
				mb.showinfo("Information", "FILE NOT SAVED, FIELDS MIGHT BE EMPTY")

# ok, do the stuff above
if __name__ == "__main__":

	app = Verses()
	app.mainloop()
