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



def csvgen(path):
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
    (27, 'accflow')
    ]
    import csv
    with open(path, 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for line in reader:
            yield {val: line[key] for key, val in headers}


class DummyScraper(ScraperBase):

    def get_data(self):
        print "Solar Hot Water must be run separately after getting the data off the SD card."
        return []

if __name__ == '__main__':
    import datetime
    import pytz
    import os
    import sys
    from commonssite.server.water.models import water
    sf = sys.argv[1]
    a = csvgen(os.path.expanduser(sf))
    path = int('20' + os.path.split(sf)[1][2:4])
    tz = pytz.timezone('America/New_York')
    counter = 1
    for x in a:
        mmdd = x.pop('MMDD')
        hhmm = x.pop('HHMM')
        timestamp = tz.localize(datetime.datetime(path, int(mmdd[0:2]), int(mmdd[2:4]), int(hhmm[0:2]), int(hhmm[2:4])))
        w = water(Time=timestamp, **x)
        w.save()
        print counter
        counter += 1

