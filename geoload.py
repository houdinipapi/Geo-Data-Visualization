import urllib.request
import urllib.parse
import urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

api_key = False
# If you have a Google Places API key, enter it here
# api_key = 'AIzaSy___IDByT70'

if api_key is False:
    api_key = 42
    serviceurl = "http://py4e-data.dr-chuck.net/json?"
else:
    serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

# Additional detail for urllib
# http.client.HTTPConnection.debuglevel = 1

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

f_hand = open("where.data")
count = 0

for line in f_hand:
    if count > 200:
        print("Retrieved 200 locations. Restart to retrieve more.")
        break

    address = line.strip()
    print('')
    cur.execute("SELECT geodata FROM Locations WHERE address= ?",
        (memoryview(address.encode()), ))

    try:
        data = cur.fetchone()[0]
        print(f"Found in database {address}")
        continue

    except:
        pass

    parms = {"address": address}

    if api_key is not False:
        parms['key'] = api_key

    url = serviceurl + urllib.parse.urlencode(parms)

    print(f"Retrieving {url}")
    uh = urllib.request.urlopen(url, context=ctx)
