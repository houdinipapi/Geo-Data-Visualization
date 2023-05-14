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


