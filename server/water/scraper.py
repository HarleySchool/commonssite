from django.db import models
from commonssite.server.water.models import water
'''
[
    (0, 'MMDD'),
    (1, 'HHMM'),
    (2, 'T1 (*C)'),
    (3, 'T2 (*C)'),
    (4, 'T3 (*C)'),
    (5, 'T4 (*C)'),
    (6, 'T5 (*C)'),
    (7, 'T7 (*C)'),
    (8, 'T8 (*C)'),
    (9, 'T9 (*C)'),
    (10, 'T10 (*C)'),
    (11, 'T11 (*C)'),
    (12, 'T12 (*C)'),
    (13, 'Flow'),
    (14, 'Pressure'),
    (15, 'Pump 1 (%)'),
    (16, 'Pump 2 (%)'),
    (17, 'Pump 3 (on/off)'),
    (18, 'Pump 4 (%)'),
    (19, 'Pump 5 (%)'),
    (20, 'Pump 6 (on/off)'),
    (21, 'Pump 7 (on/off)'),
    (22, 'Pump 8 (on/off)'),
    (23, 'Pump 9 (on/off)'),
    (24, 'Pump 10 (on/off)'),
    (25, 'Acc. NRJ'),
    (26, 'Acc. H'),
    (27, 'Acc. Flow'),
]

'''
headers = [
    (0, 'MMDD'),
    (1, 'HHMM'),
    (2, 't1'),
    (3, 't2'),
    (4, 't3'),
    (5, 't4'),
    (6, 't5'),
    (13, 'flow'),
    (14, 'pressure'),
    (15, 'pump1'),
    (16, 'pump2'),
    (17, 'pump3'),
    (25, 'accnrj'),
    (26, 'acch'),
    (27, 'accflow'),
]



def csvgen(path):
    import csv
    with open(path, 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for line in reader:
            yield {val: line[key] for key, val in headers}



if __name__ == '__main__':
    import datetime
    import pytz
    import os
    import sys
    a = csvgen(os.path.expanduser(sys.argv[1]))
    counter = 1
    path = os.path.split(sys.argv[1])[1][2:4]
    tz = pytz.timezone('America/New_York')
    for x in a:
        mmdd = x.pop('MMDD')
        hhmm = x.pop('HHMM')
        timestamp = datetime.datetime(int('20'+path), int(mmdd[0:2]), int(mmdd[2:4]), int(hhmm[0:2]), int(hhmm[2:4]))
        timestamp = tz.localize(timestamp)
        w = water(Time=timestamp, **x)
        w.save()
        print counter
        counter += 1

