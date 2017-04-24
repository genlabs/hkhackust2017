'''
Precalculate the drawing coordinates polyline for Google map 
'''
import configparser
import csv
import requests
import json
import io
import time

try:
    to_unicode = unicode
except NameError:
    to_unicode = str


#configuration
config = configparser.ConfigParser()
config.read('config.ini')
apikey = config['googlemap']['apikey']

# prepare locations
location = {}
#can combine everything in one loop, just for demo purpose

# read in all coordinate for each route
with open('tsm_link_and_node_info_v2.csv', 'rU') as csvfile:
    next(csvfile)
    trafficreader = csv.reader(csvfile)
    for row in trafficreader:
        try:
            location[row[0]] = {
                'start_node_lng' : float(row[2]),
                'start_node_lat' : float(row[3]),
                'end_node_lng': float(row[5]),
                'end_node_lat': float(row[6])
            }
        except:
            pass



# translate all cooridnates into wgs84-longtide and wgs83-latitude coordinates from hk gov
for key in location.keys():
    try:
        loc = location[key]
        response = requests.get('https://api.data.gov.hk/v1/coordinate-conversion?hk80-northing=' + str(loc['start_node_lat']) + '&hk80-easting=' + str(loc['start_node_lng']))
        data = json.loads(response.content)
        location[key]['start_node_lng'] = data['wgs84-longitude']
        location[key]['start_node_lat'] = data['wgs84-latitude']
        response = requests.get('https://api.data.gov.hk/v1/coordinate-conversion?hk80-northing=' + str(loc['end_node_lat']) + '&hk80-easting=' + str(loc['end_node_lng']))
        data = json.loads(response.content)
        location[key]['end_node_lng'] = data['wgs84-longitude']
        location[key]['end_node_lat'] = data['wgs84-latitude']
        print(location[key])
        # writer.writerow([key,location[key]['start_node_lng'],location[key]['start_node_lat'],location[key]['end_node_lng'],location[key]['end_node_lat']])
    except:
        print "Unexpected error:", sys.exc_info()[0]
    time.sleep(2)



# finish translate, now call google api to collect all routes snappoint coordinate
with io.open('data.json', 'w', encoding='utf8') as outfile:
    outfile.write(to_unicode('['))
    snap = []

    for key in location.keys():
        start_node = str(location[key]['start_node_lat']) + ',' + str(location[key]['start_node_lng'])
        end_node = str(location[key]['end_node_lat']) + ',' + str(location[key]['end_node_lng'])
        response = requests.get('https://roads.googleapis.com/v1/snapToRoads?interpolate=true&key=' + apikey + '&path=' + start_node + '|' + end_node)
        body = response.content
        snappoints = json.loads(body)
        snappointswithid = { row[0] : snappoints['snappedPoints'] }
        str_ = json.dumps(snappointswithid, separators=(',', ': '), ensure_ascii=False)
        snap.append(to_unicode(str_))

    snap_str = ',\n'.join(snap)
    outfile.write(snap_str)
    outfile.write(to_unicode(']'))
    