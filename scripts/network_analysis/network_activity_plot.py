#---------------NetworkActvityPlot---------------------#
# I. This script intends to graphically plot the network activity for
#    each device, and each session
# II. It computes some summarizing statistics values, taking
#     "csv extracts of pcap" files as inputs, and output results in csv files
#-----------Lucas O., 2020-------------#
#OS, IDE, Python : Windows 10, Atom, 3.7.0

# -*- coding: utf-8 -*-

import sys,os
import csv,json,time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
import seaborn as sns
import datetime
import string

def generateDataFrame(file,withcount=True):

    data = pd.read_csv(file,
                          encoding='utf_8',
                          sep = ';',
                          dtype = 'unicode',
                          parse_dates = True,
                          infer_datetime_format = True,
                          low_memory=False)


    data["Time"]  = pd.to_datetime(data["Time"])
    min_hour = data["Time"].min()
    max_hour = data["Time"].max()
    time_sess = (max_hour-min_hour)
    time_sess = time_sess.total_seconds()
    time_array = np.arange(np.datetime64(min_hour), np.datetime64(max_hour), np.timedelta64(1,'s'), dtype='datetime64[s]')
    data = data.drop_duplicates(subset=['Time','Destination','Protocol'])
    data = data.drop(columns=['No.','Info'])
    ip_list = data['Destination'].unique()

    print(ip_list)
    print("[+] DATA FIRST TRANSFORMED")
    print(data.head(20))

    data_time = pd.DataFrame(time_array,columns = ['time'])
    index = 1
    for ip in ip_list:
        data_time.insert(index, ip, 0, allow_duplicates=False)
        index+=1
    data_time["time"]  = pd.to_datetime(data_time["time"])
    print("[+] DATA TIME 1")
    print(data_time.head())

    if withcount == True:

        data_time.insert(index, 'count', 0, allow_duplicates=False)
        i = 0
        count = 0
        for e in data.index:
            time = data.at[e,'Time']
            ip = data.at[e,'Destination']
            for e in data_time.index:
                if time == data_time.at[e,'time']:
                    if i == 0:
                        count += 1
                        data_time.at[e,ip] = 1.0
                        data_time.at[e,'count'] += 1
                        print(time,"[+] its a match !",e,ip)
                    else:
                        count += 1
                        data_time.at[e,ip] = 1.0
                        data_time.at[e,'count'] = count
                        data_time.at[e,'count'] += 1
                        print(time,"[+] its a match !",e,ip)
                i += 1

        count = 0
        for e in data_time.index:
            if data_time.at[e,'count'] == 0:
                data_time.at[e,'count'] = count
            if data_time.at[e,'count'] > 0:
                count = data_time.at[e,'count']
        print("[+] DATA TIME 2")
        print(data_time,flush=True)

    else:
        for e in data.index:
            time = data.at[e,'Time']
            ip = data.at[e,'Destination']
            for e in data_time.index:
                if time == data_time.at[e,'time']:
                    data_time.at[e,ip] = 1.0
                    print(time,"[+] its a match !",e,ip)

        print(data_time.head(20),flush=True)
        print(data_time.shape)
        print(data_time.dtypes)

    return data_time

def HuePlot(file):

    plot_name = file[:-4]

    data = generateDataFrame(file)

    #PLOT 1 : cumulative number of communication  initiated by the IoT device
    data = generateDataFrame(file,True)
    fig2 = plt.figure(figsize=(20,5))
    ax = fig2.add_subplot(1,1,1)
    plt.title("Hue : nombre cumulé de paquets <TLS CLient Hello> et <HTTP POST> émis")
    sns.lineplot(data = data, x='time', y='count')
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.yaxis.grid(True)
    plt.ylabel("Nombre cumulé\nde paquets")
    plt.savefig(plot_name+'comm.png')
    plt.show()

    #PLOT 2 : communication per ip.dst
    data = generateDataFrame(file,False)
    fig = plt.figure(figsize=(20,5))
    ax = fig.add_subplot(1,1,1)
    plt.title("Hue : paquets <TLS CLient Hello> et <HTTP POST> émis")
    data = data.melt('time', var_name='IPs',  value_name='vals')
    sns.lineplot(data = data, x='time', y='vals',hue='IPs')
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.ylabel("Nombre par adresse IP\nde destination")
    plt.savefig(plot_name+'ip.png')
    plt.show()

    print("[+] Plots generated")

def HueStats(dataframe):

    plot_name = file[:-4]

    data = generateDataFrame(file,True)

    min_hour = data["time"].min()
    max_hour = data["time"].max()
    time_sess = (max_hour-min_hour)
    time_sess = time_sess.total_seconds()
    data = data.drop(columns=['time','count'])
    list_ip = list(data.columns[1:-1])
    count_ip = {}
    print(list_ip)
    count = 0

    #Generate a statistics summary, save it to csv 'plot_nameStats.csv''
    for ip in list_ip:
        sum = data[ip].sum()
        frequency_per_tenminutes = sum/(time_sess/600)
        frequency_per_tenminutes_rounded = str((round(frequency_per_tenminutes,2))).replace(".",",")
        count_ip[ip] = [sum, frequency_per_tenminutes_rounded]
    count_ip = {k: v for k, v in sorted(count_ip.items(), key=lambda item: item[1])}
    print(count_ip)

    data_stats = pd.DataFrame.from_dict(count_ip,orient='index',columns=['sum','freq/ten min'])
    data_stats = data_stats.sort_values(by=['sum'], ascending=False)
    print(data_stats.head())
    data_stats.to_csv(plot_name+'Stats.csv',sep = ';')

    print("[+] Stats generated")

def FireStickPlot(file):

    plot_name = file[:-4]

    data = generateDataFrame(file)

    #PLOT 1 : cumulative number of communications initiated by the IoT device
    data = generateDataFrame(file,True)
    fig2 = plt.figure(figsize=(20,5))
    ax = fig2.add_subplot(1,1,1)
    plt.title("Firestick : nombre cumulé de paquets <TLS CLient Hello> émis")
    sns.lineplot(data = data, x='time', y='count')
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.yaxis.grid(True)
    plt.ylabel("Nombre cumulé\nde paquets")
    plt.savefig(plot_name+'comm.png')
    plt.show()

    #PLOT 2 : communication per ip.dst
    data = generateDataFrame(file,False)
    fig = plt.figure(figsize=(20,5))
    ax = fig.add_subplot(1,1,1)
    plt.title("Firestick : paquets <TLS CLient Hello> émis")
    data = data.melt('time', var_name='IPs',  value_name='vals')
    sns.lineplot(data = data, x='time', y='vals',hue='IPs')
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.ylabel("Nombre par adresse IP\nde destination")
    plt.savefig(plot_name+'ip.png')
    plt.show()

    print("[+] Plots generated")

def FireStickStats(dataframe):

    plot_name = file[:-4]

    data = generateDataFrame(file,True)

    min_hour = data["time"].min()
    max_hour = data["time"].max()
    time_sess = (max_hour-min_hour)
    time_sess = time_sess.total_seconds()
    data = data.drop(columns=['time','count'])
    list_ip = list(data.columns[1:-1])
    count_ip = {}
    print(list_ip)
    count = 0

    #Generate a statistics summary, save it to csv 'plot_nameStats.csv'
    for ip in list_ip:
        sum = data[ip].sum()
        frequency_per_tenminutes = sum/(time_sess/600)
        frequency_per_tenminutes_rounded = str((round(frequency_per_tenminutes,2))).replace(".",",")
        count_ip[ip] = sum, frequency_per_tenminutes_rounded
    count_ip = {k: v for k, v in sorted(count_ip.items(), key=lambda item: item[1])}
    print(count_ip)

    data_stats = pd.DataFrame.from_dict(count_ip,orient='index',columns=['sum','freq/ten min'])
    data_stats = data_stats.sort_values(by=['sum'], ascending=False)
    print(data_stats.head())
    data_stats.to_csv(plot_name+'Stats.csv',sep = ';')

    print("[+] Stats generated")

def FamilyHubPlot(file):

    plot_name = file[:-4]

    #PLOT 1 : cumulative number of communication  initiated by the IoT device
    data = generateDataFrame(file,True)
    fig2 = plt.figure(figsize=(20,5))
    ax = fig2.add_subplot(1,1,1)
    plt.title("FamilyHub : nombre cumulé de paquets <TLS CLient Hello> émis")
    sns.lineplot(data = data, x='time', y='count')
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.yaxis.grid(True)
    plt.ylabel("Nombre cumulé\nde paquets")
    plt.savefig(plot_name+'comm.png')
    plt.show()

    #PLOT 2 : communication per ip.dst
    data = generateDataFrame(file,False)
    fig = plt.figure(figsize=(20,5))
    ax = fig.add_subplot(1,1,1)
    plt.title("FamilyHub : paquets <TLS CLient Hello> émis")
    data = data.melt('time', var_name='IPs',  value_name='vals')
    sns.lineplot(data = data, x='time', y='vals',hue='IPs')
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.ylabel("Nombre par adresse IP\nde destination")
    plt.savefig(plot_name+'ip.png')
    plt.show()

    print("[+] Plots generated")

def FamilyHubStats(file):

    plot_name = file[:-4]

    data = generateDataFrame(file,True)

    min_hour = data["time"].min()
    max_hour = data["time"].max()
    time_sess = (max_hour-min_hour)
    time_sess = time_sess.total_seconds()
    data = data.drop(columns=['time','count'])
    list_ip = list(data.columns[1:-1])
    count_ip = {}
    print(list_ip)
    count = 0

    #Generate a statistics summary, save it to csv 'plot_nameStats.csv'
    for ip in list_ip:
        sum = data[ip].sum()
        frequency_per_tenminutes = sum/(time_sess/600)
        frequency_per_tenminutes_rounded = str((round(frequency_per_tenminutes,2))).replace(".",",")
        count_ip[ip] = sum, frequency_per_tenminutes_rounded
    count_ip = {k: v for k, v in sorted(count_ip.items(), key=lambda item: item[1])}
    print(count_ip)

    data_stats = pd.DataFrame.from_dict(count_ip,orient='index',columns=['sum','freq/ten min'])
    data_stats = data_stats.sort_values(by=['sum'], ascending=False)
    print(data_stats.head())
    data_stats.to_csv(plot_name+'Stats.csv',sep = ';')

    print("[+] Stats generated")

#-------------------------------------MAIN-------------------------------------

if __name__ == "__main__":

    devicesList = ["FireStick","Samsung","Hue"]
    dstDirectory = <DST_DIR_PATH>

    start_time = time.time()

    print("[+] Start !")

        for i in range(3): #for each IoT device
            device = devicesList[i]
            srcDirectory = <SRC_DIR_PATH>+"\"+device
            print(os.getcwd())
            entries = os.listdir(srcDirectory)
            print(entries[0])

            print("[+] Import data for",device)

            if i == 0:
                for entry in entries:
                    entry_name = str(entry)
                    file = srcDirectory+entry
                    FireStickPlot(file)
                    FireStickStats(file)

            if i == 1:
                for entry in entries:
                    entry_name = str(entry)
                    file = srcDirectory+entry
                    FamilyHubPlot(file)
                    FamilyHubStats(file)

            if i == 2:
                for entry in entries:
                    entry_name = str(entry)
                    file = srcDirectory+entry
                    HuePlot(file)
                    HueStats(file)

    end_time = time.time()
    print("[+] Time required : --- %s seconds ---" % (end_time - start_time))
