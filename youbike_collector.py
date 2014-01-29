import json, httplib2, time, csv, os.path
import pandas as pd
import numpy as np
from datetime import datetime

def get_current_data():
    ''' This function consumes the youbike api to get json data on all stations. The data update every five minutes '''
    h = httplib2.Http()
    resp, content = h.request('http://210.69.61.60:8080/you/gwjs_cityhall.json')
    if not resp['status'] == '200':
        print("Warning: HTTP status not 200 OK")
    try:
        data = json.loads(content)['retVal']
    except ValueError:
        print("Error loading json")
        print("Resp: %s\nContent: %s" % (resp, content))
        return None
    return data

file_exists = os.path.isfile('youbike_data.csv')
if file_exists:
	out_csv = open('youbike_data.csv', 'a')
else:
	out_csv = open('youbike_data.csv', 'wb')
print("Starting...")
csv_writer = csv.writer(out_csv)

for i in range(12 * 24):
    data = get_current_data()
    if data:
        if not file_exists:
            header = ['time'] + [dictionary['sno'] for dictionary in data]
            csv_writer.writerow(header)
            file_exists = True

        row = [dictionary['sbi'] for dictionary in data]
        print("Data for %s" % data[0]['mday'][:-2])
        row = [data[0]['mday'][:-2]] + row
        csv_writer.writerow(row)

        time.sleep(300)


out_csv.close()

print("Done")
