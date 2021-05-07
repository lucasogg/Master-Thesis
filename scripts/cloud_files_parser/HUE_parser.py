#---------------HUEparser---------------------#
#I. Parsing "delta" and/or "config" json file obtained from the exercise
#   of the access right (15 GDPR) from Signify after the usage of the Hue
#   Lighting system (events log type)
#II. Organize & write results in a csv file
#-----------Lucas O., 2020-------------#
#OS, IDE, Python : Windows 10, Atom, 3.7.0

# -*- coding: utf-8 -*-

import json, csv
import time, base64
import os.path

table = []
count = 0

start_time = time.time()

print("[+] Start !")

print("[+] Parsing file")
with open('<SRC_FILE_PATH>.json',encoding = 'utf-8') as f:
    elem_dict = json.load(f)
    for elem in elem_dict:
        print(elem)
        if elem:
            table.append(elem)
        else:
            break

print("[+] Writing file")
with open('<DST_FILE_PATH>.csv','w',newline='') as c:
    wr = csv.writer(c, delimiter = ';')
    allHeader = set().union(*(e.keys() for e in table))
    for elem in table:
        if count == 0 :
            wr.writerow(allHeader)
            print(allHeader)
        count += 1
        print(elem)
        e = str(elem.values())
        wr.writerow([elem.get(h,None)for h in allHeader])

end_time = time.time()
print("[+] Time required : --- %s seconds ---" % (end_time - start_time))
