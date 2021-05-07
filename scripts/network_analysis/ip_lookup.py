#---------------IPLookUp---------------------#
#I. This script first extracts src & dst IPv4 adresses from a csv file
#   (exported from a pcap file)
#II. It provides results of automated ip_whois requests for these adresses,
#    thanks to the ipwhois library
#III. The processed results are finally written into a csv file
#-----------Lucas O., 2020-------------#
#OS, IDE, Python : Windows 10, Atom, 3.7.0

# -*- coding: utf-8 -*-

import sys,os
from ipwhois import IPWhois
from ipwhois.utils import get_countries
import ipwhois
import csv,json,time
import pandas as pd
import numpy as np
from datetime import datetime

def ipLookup(ip):
    results = []
    try:
        obj = ipwhois.IPWhois(ip)
        result = obj.lookup_whois()
        desc = result['nets']
        desc = desc[0]
        description = result['asn_description']
        description2 = desc['description']
        country = result['asn_country_code']
        state = desc['state']
        city = desc['city']
        results = [ip,description,description2,state,country,city]
        print(result,flush=True)
        print(results, flush=True)
    except ipwhois.exceptions.IPDefinedError:
        print("<!> Error received", flush=True)
        return None
    return results

#-------------------------------------MAIN-------------------------------------

if __name__ == "__main__":

    dstDirectory = <DST_DIR_PATH>
    srcDirectory = <SRC_DIR_PATH>
    print(os.getcwd())
    entries = os.listdir(srcDirectory)
    print(entries)

    start_time = time.time()

    print("[+] Start !", flush=True)

    for entry in entries :
        ip_list = []
        i = 0
        df = pd.read_csv(srcDirectory+entry,sep=",")
        df = df.filter(items=["Source", "Destination"])
        print(df.shape, flush=True)
        IPsrc = df["Source"].unique()
        IPdst = df["Destination"].unique()
        for adress in IPsrc:
            ip_list.append(adress)
        for adress in IPdst:
            ip_list.append(adress)
        ip_list = set(ip_list)
        print(ip_list)
        print("IP Set done", flush=True)

        count = 0
        print("[+] Why not write them", flush=True)
        with open(dstDirectory+entry,'w',newline='') as c:
            wr = csv.writer(c, delimiter = ';')
            allHeader = ["IP","Description","Additional","State","Country","City"]
            wr.writerow(allHeader)
            print("[+] Header of processed csv written...loading", flush=True)
            for ip in ip_list:
                res = ipLookup(ip)
                if res is None:
                    pass
                else:
                    try:
                        wr.writerow(res)
                    except csv.Error as error:
                        print("NoneType", flush=True)

        print("[+] ",entry,": IPs looked up and written", flush=True)
        i += 1

    end_time = time.time()
    print("[+] Time required : --- %s seconds ---" % (end_time - start_time))
