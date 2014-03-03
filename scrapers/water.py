# dependancies
import csv
headers = ["MMDD",
"HHMM",
"T1 (*C)",
"T2 (*C)",
"T3 (*C)",
"T4 (*C)",
"T5 (*C)",
"T7 (*C)",
"T8 (*C)",
"T9 (*C)",
"T10 (*C)",
"T11 (*C)",
"T12 (*C)",
"Flow",
"Pressure",
"Pump 1 (%)",
"Pump 2 (%)",
"Pump 3 (on/off)",
"Pump 4 (%)",
"Pump 5 (%)",
"Pump 6 (on/off)",
"Pump 7 (on/off)",
"Pump 8 (on/off)",
"Pump 9 (on/off)",
"Pump 10 (on/off)",
"Acc. NRJ",
"Acc. H",
"Acc. Flow"]
# For parsing semicolon delimited CSV into a dict with a list containing the row values
# Designed especially for a .dat file outputted by a watts solar water heater controller

# path is the path to your .dat file
def main(path):
	lines = {}
	thelist = []
	# open the file
	with open(path,"rU") as csvfile:
		# Make the csv reader object
		reader = csv.reader(csvfile, delimiter=";", quotechar="|")
		# iterate over the rows in the table
		for row in reader:
			print zip(headers, row)

# if this is the file being exacuted
if __name__ == "__main__":
	# Import some stuff
	from pprint import pprint
	import sys
	# Print nicely the returned dict
	# sys.argv[1] is the first command line argument 
	pprint(main(sys.argv[1]))