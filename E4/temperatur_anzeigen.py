import streamlit as st
from algorithm import Algorithm

class TemperaturAnzeigen(Algorithm):
    def __init__(self) -> None:
        self.tmp = None

    def compute(self, data_dict):
        self.tmp = data_dict["Tmp"][-1][1]

    def visualize(self, window):
        with window:
            st.metric(label="Temperature",value=self.tmp)
