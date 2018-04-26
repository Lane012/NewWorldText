from tkinter import *


class mainWindow:
	"""the main window of the text editor this file contains all gui components"""
	row_column = ''
	keywords = ('if', 'def')
	def __init__(self):
		self.root = Tk()
		self.body = Text(self.root, highlightbackground='#00FF00', highlightcolor='#00FF00', 
						selectbackground='#00FF00', background='black', foreground='green')
		self.body.tag_configure("b", foreground='blue')
		self.body.tag_configure("o", foreground='purple')
		self.body.bind('<Key>', self.highlight)
		self.body.pack()
		self.start()


	def undo(self, event):
		self.body.edit_undo() 

	
	def highlight(self, event):
		if self.body.edit_modified():
			self.body.edit_modified(False)
			text = self.getCurrentLineOfText(event)
			self.textChecker(text)

	def getCurrentLineOfText(self, event):
		self.row_column= self.body.index("insert").split(".")
		current_line = self.body.get(self.row_column[0] + ".0", END).strip("\n")
		current_line += event.char
		return current_line

	def textChecker(self, text: str):
		try:
			start_index, keyword = self.checkForKeyword(self.getFormatedRowColumn(self.row_column))
		except:
			return

		if start_index:
			end_index = start_index.split(".")
			end_index[1] = str(int(end_index[1]) + len(keyword))
			self.body.delete(start_index, self.getFormatedRowColumn(end_index))
			self.body.insert(start_index, keyword, 'o')

	
	def getFormatedRowColumn(self, row_column):
		return "%s.%s" % (row_column[0], row_column[1])

	def checkForKeyword(self, positionInLine):
		for keyword in self.keywords:
			index = self.body.search(keyword, positionInLine, backwards=True, exact=True, stopindex=positionInLine + "-" + str(len(keyword)) +"c")
			if index:
				return (index, keyword)
		

	def start(self):
		self.root.mainloop()




main = mainWindow()