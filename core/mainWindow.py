from tkinter import *


class mainWindow:
	"""the main window of the text editor this file contains all gui components"""
	row_column = ''
	keywords = {'if': 'p', 'def': 'b', '==': 'p','\w+(\()': 'g', '>': 'p', '!=': 'p', 'class': 'b', 'self': 'o', 'return': 'p', '=': 'p', '\'': 'o'}
	def __init__(self):
		self.root = Tk()
		self.root.title("NewWorldText")

		self.menu_bar = Menu(self.root, background="white", font= ('Tempus Sans ITC', 14))
		
		self.filemenu = Menu(self.menu_bar)
		self.filemenu = Menu(self.menu_bar, tearoff=0)
		self.filemenu.add_command(label="New", command=None)
		self.filemenu.add_command(label="Open", command=None)
		self.filemenu.add_command(label="Save", command=None)
		self.filemenu.add_command(label="Save as...", command=None)
		self.filemenu.add_command(label="Close", command=None)

		self.menu_bar.add_cascade(label="File", menu=self.filemenu)
		self.root.config(menu=self.menu_bar)

		self.body = Text(self.root, selectbackground='#00FF00', background='#303030', foreground='white')
		self.body.tag_configure("b", foreground='#0246d6')
		self.body.tag_configure("p", foreground='purple')
		self.body.tag_configure('g', foreground='green')
		self.body.tag_configure("o", foreground='#df5a00')
		self.body.bind('<Key>', self.highlight)
		self.body.bind("<Tab>", self.tab)
		self.body.pack()

		self.start()

	def tab(self, event):
		self.body.insert("insert", " " * 4)

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
		positionInLine = self.getFormatedRowColumn(self.row_column)
		try:
			start_index, keyword = self.checkForKeyword(positionInLine)
		except:
			return

		if start_index:
			is_regex, end_index = self.getEndIndex(positionInLine, start_index, keyword)
			text = self.body.get(start_index, end_index)
			self.body.delete(start_index, end_index)
			
			if is_regex:
				self.body.insert(start_index, text, self.keywords[keyword])
			else:
				self.body.insert(start_index, keyword, self.keywords[keyword])

	
	def isRegex(self, keyword):
		return keyword == '\w+(\()'

	def getEndIndex(self, positionInLine, start_index, keyword):
		if self.isRegex(keyword):
				end_index = self.body.search("(", positionInLine, backwards=True, exact=True, stopindex=positionInLine + '-1c')
		else:
			end_index = start_index.split(".")
			end_index[1] = str(int(end_index[1]) + len(keyword))
			end_index = self.getFormatedRowColumn(end_index)
		
		return (self.isRegex(keyword), end_index)



	def getFormatedRowColumn(self, row_column):
		return "%s.%s" % (row_column[0], row_column[1])

	def checkForKeyword(self, positionInLine):
		for keyword in self.keywords.keys():
			index = self.body.search(keyword, positionInLine, backwards=True, exact=True, stopindex=positionInLine + "-" + str(len(keyword)) +"c", regexp=self.isRegex(keyword))

			if self.tabSpaceOrBeginningOfLine(index): 
				return (index, keyword) 
		
	def tabSpaceOrBeginningOfLine(self, index):
		if index:
			if self.body.get(index + "-1c") == ' ' or self.body.get(index + "-1c") == '\t': #space or tab before keyword 
				return True
			if index[2] == '0': #keyword at beginning of line
				return True
		return False

	def start(self):
		self.root.mainloop()




main = mainWindow()