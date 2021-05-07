#---------------FSparser---------------------#
#I. Parsing json files obtained from the exercise of the access right (15 GDPR)
#   from Amazon after the usage of the Firestick device (events log type)
#II. For each file of src directory : organize & write results in a csv file
#-----------Lucas O., 2020-------------#
#OS, IDE, Python version : Windows 10, Atom, 3.7.0

# -*- coding: utf-8 -*-

import json, csv
import time, base64
import os

table = []
count = 0
srcDirectory = <SRC_DIR_PATH>

start_time = time.time()

print("[+] Start !")

for filename in os.listdir(srcDirectory) :

    print("[+] Parsing file")
    with open(srcDirectory+"/"+filename) as f:
        for line in f:
            table.append(json.loads(line))

    print("[+] Writing file")
    count = 0
    with open(<DST_FILE_PATH>+filename+'.csv','w',newline='') as c:
        wr = csv.writer(c, delimiter = ';')
        allHeader = set().union(*(e.keys() for e in table))
        for elem in table:
            if count == 0 :
                wr.writerow(allHeader)
                print(allHeader)
            count += 1
            print(elem)
            e = str(elem.values())
            wr.writerow([elem.get(h,None) for h in allHeader])

end_time = time.time()
print("[+] Time required : --- %s seconds ---" % (end_time - start_time))
