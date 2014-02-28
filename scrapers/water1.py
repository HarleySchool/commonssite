# Version .1
# Changes from alpha:
# changed key to an int of the form MMDDHHMM
# Features:
# parse .dat output of a watts electric solar water controller

import csv

def main(path, key):
	t1 = {}
	t2 = {}
	t3 = {}
	t4 = {}
	t5 = {}
	t6 = {}
	t7 = {}
	t8 = {}
	t9 = {}
	t10 = {}
	t11 = {}
	t12 = {}
	flow = {}
	pressure = {}
	pump1 = {}
	pump2 = {}
	pump3 = {}
	pump4 = {}
	pump5 = {}
	pump6 = {}
	pump7 = {}
	pump8 = {}
	pump9 = {}
	pump10 = {}
	accnrj = {}
	acch = {}
	accflow = {}
	with open(path, 'rU') as csvfile:
		reader = csv.reader(csvfile, delimiter=';', quotechar='|')
		for row in reader:
			datetime = int(str(row[0] + row[1]))
			t1[datetime] = row[2]
			t2[datetime] = row[3]
			t3[datetime] = row[4]
			t4[datetime] = row[5]
			t5[datetime] = row[6]
			t7[datetime] = row[7]
			t8[datetime] = row[8]
			t9[datetime] = row[9]
			t10[datetime] = row[10]
			t11[datetime] = row[11]
			t12[datetime] = row[12]
			flow[datetime] = row[13]
			pressure[datetime] = row[14]
			pump1[datetime] = row[15]
			pump2[datetime] = row[16]
			pump3[datetime] = row[17]
			pump4[datetime] = row[18]
			pump5[datetime] = row[19]
			pump6[datetime] = row[20]
			pump7[datetime] = row[21]
			pump8[datetime] = row[22]
			pump9[datetime] = row[23]
			pump10[datetime] = row[24]
			accnrj[datetime] = row[25]
			acch[datetime] = row[26]
			accflow[datetime] = row[27]
		print "At " + str(key)
		print 'T1 was ' + str(t1[key]) + " degrees C"
		print 'T2 was ' + str(t2[key]) + " degrees C"
		print 'T3 was ' + str(t3[key]) + " degrees C"
		print 'T4 was ' + str(t4[key]) + " degrees C"
		print 'T5 was ' + str(t5[key]) + " degrees C"
		#print 'T6 was ' + str(t6[key]) + " degrees C"
		print 'T7 was ' + str(t7[key]) + " degrees C"
		print 'T8 was ' + str(t8[key]) + " degrees C"
		print 'T9 was ' + str(t3[key]) + " degrees C"
		print 'T10 was ' + str(t10[key]) + " degrees C"
		print 'T11 was ' + str(t11[key]) + " degrees C"
		print 'T12 was ' + str(t12[key]) + " degrees C"
		print 'Flow was ' + str(flow[key])
		print 'Pressure was ' + str(pressure[key])
		print 'Pump 1 was ' + str(pump1[key]) + " %"
		print 'Pump 2 was ' + str(pump2[key]) + " %"
		print 'Pump 3 was ' + str(pump3[key])
		print 'Pump 4 was ' + str(pump4[key]) + " %"
		print 'Pump 5 was ' + str(pump5[key]) + " %"
		print 'Pump 6 was ' + str(pump6[key])
		print 'Pump 7 was ' + str(pump7[key])
		print 'Pump 8 was ' + str(pump8[key])
		print 'Pump 9 was ' + str(pump9[key])
		print 'Pump 10 was ' + str(pump10[key])
		print 'Acc. NRJ was ' + str(accnrj[key])
		print 'Acc H. was ' + str(acch[key])
		print 'Acc. Flow was ' + str(accflow[key])


if __name__ == '__main__':
	import sys
	from pprint import pprint
	main(sys.argv[1], int(sys.argv[2]))
