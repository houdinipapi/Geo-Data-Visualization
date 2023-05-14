import sqlite3
import json
import codecs

# Creating connection
conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

# Executing the cursor
cur.execute('SELECT * FROM Locations')

# Opening and writing a file
f_hand = codecs.open('where.js', 'w', 'utf-8')
f_hand.write("myData = [\n")

# Initializing count
count = 0

# Iterating the database
for row in cur:
    data = str(row[1].decode())

    try:
        js = json.loads(str(data))
    except:
        continue

    if not ('status' in js and js['status'] == 'OK'):
        continue

    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]

    if lat == 0 or lng == 0:
        continue

    where = js['results'][0]['formatted_address']
    where = where.replace("'", "")

    try:
        print(where, lat, lng)

        count += 1
        if count > 1:
            f_hand.write(",\n")

        output = "["+str(lat)+", "+str(lng)+", '"+where+"']"
        f_hand.write(output)

    except:
        continue

f_hand.write("\n];\n")
cur.close()
f_hand.close()
print(f"{count} records written to where.js")
print("Open where.html to view in a browser")
