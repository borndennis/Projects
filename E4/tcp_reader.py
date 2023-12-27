import socket
import time
import csv
import numpy as np
import pandas as pd
from datetime import datetime, timezone
import streamlit as st
from data_completeness import DataCompleteness
from temperatur_anzeigen import TemperaturAnzeigen
from movement_detection import MovementDetection



HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 28001  # The port used by the server
            

def process_data():
    
    #gecleante Sensordaten werden in dictionary gespeichert
    data_dict = {"Acc":[],
                "Gsr":[],
                "HR":[],
                "Tmp":[],
                "Bvp":[]}

    #Objekte erstellen um später Funktionen aufzurufen
    data_completeness = DataCompleteness()
    temperatur_anzeigen = TemperaturAnzeigen()
    movement_detection = MovementDetection()


    placeholder = st.empty()    
    while True:
        with placeholder.container():
            col1, col2, col3 = st.columns(3)

            #Daten werden 2 Sekunden lang gesammelt bevor sie verarbeitet werden
            time.sleep(2)
            
            #Cleaning
            data = s.recv(32768)
            data=str(data)[2:-1] 
            data=data.split("\\r\\n")
            data=data[:-1]
            for message in data:
                message = message.replace(",",".")
                elements = message.split(" ")

                # 0. Element: Sensor
                sensor = elements[0]
                sensor = sensor.replace("E4_","")

                # 1. Element: Zeit
                zeit_str = elements[1]
                if "device_subscribe" in zeit_str:
                    continue
                zeit=float(zeit_str)

                # 2. Element: Wert (Acc hat 3 Werte)
                if "Acc" in sensor:
                    wert = [elements[2],elements[3],elements[4]] 
                else:
                    wert = elements[2]
                
                # Daten hinzufügen zum Dictionary
                # Keys=Sensoren, Values=Liste die aus Zeit/Wert-Paaren (wieder Listen) besteht
                if "Acc" in sensor:
                    data_dict["Acc"].append([zeit,wert]) 
                if "Gsr" in sensor:
                    data_dict["Gsr"].append([zeit,wert]) 
                if "Ibi" in sensor:
                    data_dict["HR"].append([zeit,wert]) 
                if "Temperature" in sensor:
                    data_dict["Tmp"].append([zeit,wert]) 
                if "Bvp" in sensor:
                    data_dict["Bvp"].append([zeit,wert]) 

            #1. Funktionsaufruf
            data_completeness.compute(data_dict)
            data_completeness.visualize(col1)

            #2. Funktionsaufruf
            movement_detection.compute(data_dict)
            movement_detection.visualize(col2)

            #3. Funktionsaufruf
            temperatur_anzeigen.compute(data_dict)
            temperatur_anzeigen.visualize(col3)
        
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # s.sendall(b"device_list \r\n")
    # print(s.recv(8192))

    # s.sendall(b"device_connect BE9CFD \r\n")
    # s.sendall(b"device_connect A01C99 \r\n")
    s.sendall(b"device_connect 1A4D5C \r\n")
    data = s.recv(8192)

    subscribe="device_subscribe "+"gsr"+" on \r\n"
    subscribe=subscribe.encode("UTF-8")
    s.sendall(subscribe)
    data = s.recv(8192)

    subscribe="device_subscribe "+"acc"+" on \r\n"
    subscribe=subscribe.encode("UTF-8")
    s.sendall(subscribe)
    data = s.recv(8192)

    subscribe="device_subscribe "+"ibi"+" on \r\n"
    subscribe=subscribe.encode("UTF-8")
    s.sendall(subscribe)
    data = s.recv(8192)

    subscribe="device_subscribe "+"tmp"+" on \r\n"
    subscribe=subscribe.encode("UTF-8")
    s.sendall(subscribe)
    data = s.recv(8192)

    subscribe="device_subscribe "+"bvp"+" on \r\n"
    subscribe=subscribe.encode("UTF-8")
    s.sendall(subscribe)
    data = s.recv(8192)
    
    process_data()

        


    