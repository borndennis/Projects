import streamlit as st
from algorithm import Algorithm
import tensorflow as tf
import csv
import numpy as np

class MovementDetection(Algorithm):
    def __init__(self):
        self.model = tf.saved_model.load("trainedmodel")
        self.prediction = None
        self.acc = [[]]

    def compute(self, data_dict):
        #Accelerometer Daten in Liste darstellen, und an trainiertes model als Input übergeben
        self.acc = np.asarray(data_dict["Acc"][-1][1], dtype=np.float32)[None, :]
        model_input = tf.convert_to_tensor(self.acc, dtype=tf.float32)
        print(model_input)
        model_output = self.model(model_input)
        print(model_output)
        #Argument mit höherer Wahrscheinlichkeit "Movement" oder "No Movement" wird ausgegeben
        self.prediction = tf.math.argmax(model_output[0]).numpy()
        print(self.prediction)

    def visualize(self, window):
        with window:
            st.metric(label="Prediction",value=self.prediction)
    