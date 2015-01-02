#!/usr/bin/python3.4


def test_bar(args):
    import progress_bar
    import time
    pb = progress_bar.ProgressBar(**args)
    pb.begin()
    for i in range(args["task_number"]):
        pb.add_progress()
        #time.sleep(0.1)
    print()

arguments = dict(task_number = 100000)

print("Simple progress bar :")
test_bar(arguments)

print("Simple progress bar without absolute progress :")
arguments["display_absolute_progress"] = False
test_bar(arguments)

print("Simple progress bar without percentage :")
arguments["display_absolute_progress"] = True
arguments["display_percent"] = False
test_bar(arguments)

print("Custom bars with custom filled/empty char, when more than one char is given, the result is truncated :")
arguments["display_percent"] = True
arguments["empty_char"] = " /"
arguments["filled_char"] = ":."
test_bar(arguments)

arguments["empty_char"] = "~"
arguments["filled_char"] = "#"
test_bar(arguments)

print("Custom bar with custom begin/end char :")
arguments["bar_opening"] = "°°~<[|"
arguments["bar_ending"] = "|]>~°°"
arguments["empty_char"] = "-"
arguments["filled_char"] = "="
test_bar(arguments)

print("Custom shorter bar :")
arguments["filled_char"] = "~"
arguments["bar_length"] = 80
test_bar(arguments)

print("Front char:")
arguments["enable_front_char"] = True
test_bar(arguments)
arguments["front_char"] = "|"
test_bar(arguments)

print("Changing the update rate :")
arguments["update_rate"] = 10000
test_bar(arguments)

# WARNING : increasing the precision with no update rate set may result
# in the bar being reprinted at each iteration (because the percentage
# would change every time) and thus slowing your process, it is recommended
# to have a not to high precision compared to the number of tasks to
# perform or to set an update rate
print("Changing decimal precision of percentage :")
arguments["percent_precision"] = 0
test_bar(arguments)
