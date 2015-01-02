#!/usr/bin/python3.4

def testBar(args):
	import progress_bar
	pb = progress_bar.ProgressBar(**args)
	pb.begin()
	for i in range(args["actionsCount"]):
		pb.addProgress()
	print()

arguments = dict(actionsCount = 50000)

print("Simple progress bar :")
testBar(arguments)

print("Simple progress bar without absolute progress :")
arguments["display_abs_prog"] = False
testBar(arguments)

print("Simple progress bar without percentage :")
arguments["display_abs_prog"] = True
arguments["display_perc"] = False
testBar(arguments)

print("Custom bars with custom filled/empty char, when more than one char is given, the result is truncated :")
arguments["display_perc"] = True
arguments["empty_char"] = " /"
arguments["filled_char"] = ":."
testBar(arguments)

arguments["empty_char"] = "~"
arguments["filled_char"] = "#"
testBar(arguments)

print("Custom bar with custom begin/end char :")
arguments["bar_begins"] = "°°~<[|"
arguments["bar_ends"] = "|]>~°°"
arguments["empty_char"] = "-"
arguments["filled_char"] = "="
testBar(arguments)

print("Custom shorter bar :")
arguments["filled_char"] = "~"
arguments["bar_length"] = 80
testBar(arguments)

print("Front char:")
arguments["enable_front_char"] = True
testBar(arguments)
arguments["front_char"] = "|"
testBar(arguments)

print("Changing the update rate :")
arguments["update_rate"] = 10000
testBar(arguments)

# WARNING : increasing the precision with no update rate set may result
# in the bar being reprinted at each iteration (because the percentage
# would change every time) and thus slowing your process, it is recommended
# to have a not to high precision compared to the number of tasks to
# perform or to set an update rate
print("Changing decimal precision of percentage :")
arguments["perc_digits"] = 0
testBar(arguments)
