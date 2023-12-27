from datetime import datetime, timezone
import time
import pandas as pd
import streamlit as st
from algorithm import Algorithm

class DataCompleteness(Algorithm):
    def __init__(self) -> None:
        #Dataframe wird zur Visualisierung der Daten in Streamlit genutzt
        self.df1 = pd.DataFrame(columns=["Time/seconds",
                                "Accelerometer",
                                "Galvanic Skin Response",
                                "Heart Rate",
                                "Temperature",
                                "Blood Volume Pulse"])
        
        #Startzeit nehmen um X-Achse zu visualisieren
        self.start_time = datetime.now(timezone.utc).timestamp()

    def compute(self, data_dict):

        #Samples werden pro Zeitfenster aufgezählt
        acc_samples = 0
        gsr_samples = 0
        hr_samples = 0
        tmp_samples = 0
        bvp_samples = 0

        #Zeitdaten aus data_dict werden werden in einzelne Listen übergeben
        acc_times = []
        gsr_times = []
        hr_times = []
        tmp_times = []
        bvp_times = []

        for i in range(len(data_dict["Acc"])):
            acc_times.append(data_dict["Acc"][i][0])
        for i in range(len(data_dict["Gsr"])):
            gsr_times.append(data_dict["Gsr"][i][0])
        for i in range(len(data_dict["HR"])):
            hr_times.append(data_dict["HR"][i][0])
        for i in range(len(data_dict["Tmp"])):
            tmp_times.append(data_dict["Tmp"][i][0])
        for i in range(len(data_dict["Bvp"])):
            bvp_times.append(data_dict["Bvp"][i][0])

        #Zeitfenster der letzten 6 bis 3 Sekunden vorher
        timestamp_0 = datetime.now(timezone.utc).timestamp()
        timestamp_1 = timestamp_0 - 3
        timestamp_2 = timestamp_0 - 6

        #Prüfen ob Zeitdaten in Zeitfenster liegen und Samples zählen
        for val in acc_times:
            if val<timestamp_1 and val>timestamp_2:
                acc_samples+=1
        for val in gsr_times:
            if val<timestamp_1 and val>timestamp_2:
                gsr_samples+=1
        for val in hr_times:
            if val<timestamp_1 and val>timestamp_2:
                hr_samples+=1
        for val in tmp_times:
            if val<timestamp_1 and val>timestamp_2:
                tmp_samples+=1
        for val in bvp_times:
            if val<timestamp_1 and val>timestamp_2:
                bvp_samples+=1

        #Ist/Soll-Verhältnis in % bestimmen und in neuem Dataframe vereinen
        df2 = pd.DataFrame([[timestamp_0 - self.start_time,
                            acc_samples*100/96,
                            gsr_samples*100/12,
                            hr_samples*100/3,
                            tmp_samples*100/12,
                            bvp_samples*100/192]],
                            columns=["Time/seconds",
                                        "Accelerometer",
                                        "Galvanic Skin Response",
                                        "Heart Rate",
                                        "Temperature",
                                        "Blood Volume Pulse"])
        
        #neues Dataframe an erstes anfügen 
        #immer länger werdende Liste aus Completeness-Daten entsteht
        self.df1 = pd.concat([self.df1, df2]).reset_index(drop=True)


    def visualize(self, window):
        with window:
            st.title('Verifying data completeness (%) for E4\'s multiple data streams')
            st.line_chart(self.df1.iloc[-14:], 
                        x="Time/seconds", 
                        y=["Accelerometer",
                            "Galvanic Skin Response",
                            "Heart Rate",
                            "Temperature",
                            "Blood Volume Pulse"],
                        #color=["#FF0000","#0000FF","#ffa600","#00ffbb","#d400ff"],
                        use_container_width=False)
