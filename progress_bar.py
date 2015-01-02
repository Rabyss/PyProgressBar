#!/usr/bin/python3.4

class ProgressBar:
	__BAR_BEGINS = '['
	__EMPTY_PROGRESS_CHAR = '-'
	__FILLED_PROGRESS_CHAR = '='
	__BAR_ENDS = ']'

	__BAR_LENGTH = 10
	__TOTAL_ACTIONS = 100
	
	__CUR_PROGRESS = 0
	__CUR_LENGTH = 0

	__UPDATE_RATE = 0
	__UPDATE_COUNT = 0

	__PERC_DIGITS = "1"

	__DISPLAY_PERC = True
	__DISPLAY_ABS_PROG = True
	
	__ENABLE_FRONT_CHAR = False
	__FRONT_CHAR = ">"

	def __init__(self, actionsCount, bar_begins = "[", bar_ends = "]", empty_char = "-", filled_char = "=", 
	update_rate = 0, perc_digits = 1, display_perc = True, display_abs_prog = True, bar_length = 0,
	enable_front_char = False, front_char = ">"):
		import sys
		self.__TOTAL_ACTIONS = actionsCount
		self.__BAR_BEGINS = bar_begins
		self.__BAR_ENDS = bar_ends
		self.__EMPTY_PROGRESS_CHAR = empty_char
		if len(self.__EMPTY_PROGRESS_CHAR) == 0:
			print("EMPTY_CHAR must be one character.")
			sys.exit(-1)
		elif len(self.__EMPTY_PROGRESS_CHAR) > 1:
			print("EMPTY_CHAR truncated to size one.")
			self.__EMPTY_PROGRESS_CHAR = self.__EMPTY_PROGRESS_CHAR[0]

		self.__FILLED_PROGRESS_CHAR = filled_char
		if len(self.__FILLED_PROGRESS_CHAR) == 0:
			print("FILLED_CHAR must be one character.")
			sys.exit(-1)
		elif len(self.__FILLED_PROGRESS_CHAR) > 1:
			print("FILLED_CHAR truncated to size one.")
			self.__FILLED_PROGRESS_CHAR = self.__FILLED_PROGRESS_CHAR[0]

		self.__UPDATE_RATE = update_rate
		self.__PERC_DIGITS = str(perc_digits)
		self.__DISPLAY_PERC = display_perc
		self.__DISPLAY_ABS_PROG = display_abs_prog
		if bar_length > 0:
			self.__BAR_LENGTH = min(bar_length, self.__computeMaxLength())
		else:
			self.__BAR_LENGTH = self.__computeMaxLength()
		
		self.__ENABLE_FRONT_CHAR = enable_front_char
		
		self.__FRONT_CHAR = front_char
		if len(self.__FRONT_CHAR) == 0:
			print("FRONT_CHAR must be one character.")
			sys.exit(-1)
		elif len(self.__FRONT_CHAR) > 1:
			print("FRONT_CHAR truncated to size one.")
			self.__FRONT_CHAR = self.__FRONT_CHAR[0]


	def begin(self):
		self.__UPDATE_COUNT = 0
		self.__CUR_LENGTH = 0
		self.__CUR_PROGRESS = 0
		print(self.__getBarString(), end='\r')

	def addProgress(self, inc = 1):
		increment = inc if inc > 0 else 1
		if self.__CUR_PROGRESS < self.__TOTAL_ACTIONS:
			prevPercent = self.__getStringPercentProgress()
			self.__CUR_PROGRESS = min(self.__TOTAL_ACTIONS, self.__CUR_PROGRESS + increment)
			self.__UPDATE_COUNT += increment
			newLength = int(self.__getFloatProgress() * self.__BAR_LENGTH)
			needToUpdate = False
			if self.__UPDATE_RATE > 0:
				needToUpdate = self.__UPDATE_COUNT >= self.__UPDATE_RATE
			else:
				needToUpdate = newLength > self.__CUR_LENGTH or prevPercent != self.__getStringPercentProgress()
			if needToUpdate or self.__CUR_PROGRESS == self.__TOTAL_ACTIONS:
				self.__UPDATE_COUNT = 0
				self.__CUR_LENGTH = newLength
				endChar = "\r" if self.__CUR_PROGRESS < self.__TOTAL_ACTIONS else "\n"
				print(self.__getBarString(), end = endChar)
	
	def __getFloatProgress(self):
		return float(float(self.__CUR_PROGRESS)/float(self.__TOTAL_ACTIONS))

	def __getStringPercentProgress(self):
		format = "{0:." + self.__PERC_DIGITS + "f}"
		return format.format(self.__getFloatProgress()*100) + "%"
	
	def __getStringProgressFraction(self):
		return str(self.__CUR_PROGRESS) + "/" + str(self.__TOTAL_ACTIONS)

	def __getBarString(self):
		diff = self.__BAR_LENGTH - self.__CUR_LENGTH - (1 if self.__ENABLE_FRONT_CHAR else 0)
		progresses = ""
		if self.__DISPLAY_PERC:
			progresses += " : " + self.__getStringPercentProgress()
			progresses += " (" + self.__getStringProgressFraction() + ")" if self.__DISPLAY_ABS_PROG else ""
		elif self.__DISPLAY_ABS_PROG:
			progresses += " : " + self.__getStringProgressFraction()
		front_char = self.__FRONT_CHAR if (self.__ENABLE_FRONT_CHAR and self.__CUR_PROGRESS < self.__TOTAL_ACTIONS) else ""
		return self.__BAR_BEGINS + self.__CUR_LENGTH * self.__FILLED_PROGRESS_CHAR + front_char + diff * self.__EMPTY_PROGRESS_CHAR + self.__BAR_ENDS + progresses
	
	def __computeMaxLength(self):
		import os
		env = os.environ
		def ioctl_GWINSZ(fd):
			try:
				import fcntl, termios, struct, os
				cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
			except:
				return
			return cr
		cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
		if not cr:
			try:
				fd = os.open(os.ctermid(), os.O_RDONLY)
				cr = ioctl_GWINSZ(fd)
				os.close(fd)
			except:
				pass
		if not cr:
			cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
		
		max_length = int(cr[1])
		max_length -= (len(str(self.__TOTAL_ACTIONS))*2 + 1) if self.__DISPLAY_ABS_PROG else 0
		max_length -= len(self.__BAR_BEGINS)
		max_length -= len(self.__BAR_ENDS)
		max_length -= (5 + int(self.__PERC_DIGITS)) if self.__DISPLAY_PERC else 0
		max_length -= 1 if int(self.__PERC_DIGITS) > 0 else 0
		max_length -= 3 if (self.__DISPLAY_PERC and self.__DISPLAY_ABS_PROG) else 0
		max_length -= 2 if (self.__DISPLAY_PERC or self.__DISPLAY_ABS_PROG) else 0
		return max_length

if __name__ == "__main__":
	print("Fast bar : ")
	progressBar = ProgressBar(100000,bar_begins="\\", bar_ends="/", empty_char = "_", filled_char = "#")
	progressBar.begin()
	for i in range(25000):
		progressBar.addProgress(4)
	print("Reset then relaunch :")
	progressBar.begin()
	for i in range(25000):
		progressBar.addProgress(4)
