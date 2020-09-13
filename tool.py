import sys,os

"""author : sawyerf"""
import sys,os

def stdout(message):
    sys.stdout.write(message)
    sys.stdout.write('\b' * len(message))   # \b: non-deleting backspace


class Progress():
	"""Print a progress bar"""
	def __init__(self,string, xmax=0):
		row, column = os.popen("stty size", "r").read().split()
		self.column = int(column)
		self.xmin = 0
		self.xmax = xmax
		self.string = string

	def add(self):
		self.xmin += 1
		self.progress_bar()

	def progress_bar(self):
		load = ''
		if self.xmax == 0:
			pc = 0
		else:
			pc = (self.xmin/self.xmax)
		for i in range(int(pc*40)):
			load += '█'
		for i in range(int(40 - pc * 40 + (pc * 40) % 1)):
			load += ' '
		stri = ('{} %|{}| {}/{}').format(str(pc*100)[:3], load, str(self.xmin), str(self.xmax), end='\r')
		stri = stri.rjust(self.column)
		stdout(stri)
		stdout('{} '.format(self.string)) 
		sys.stdout.flush()
		print('',end='\r')
		if pc == 1:
			print()
