In this section you can find my first big python project. 
A university project in which I had to handle sensor data transmitted by a medical device.
I took me a about 5 months to program.
It's purpose is to collect and process data sent by a wrist watch to a TCP-Server via Bluetooth LE.
Multiple functionalities are included in this program:

	- Connecting to the TCP-Server using the Socket framework
	- Deconstruction of incoming datastrings which contain biometric sensor data collected by wrist watch (Accelerometer, Skin temperature, Blood Pulse, etc.)
	- Rearranging the data in a dictionary
	- Visualization of data completeness in a line chart using the streamlit application (calculations made with a given sampling frequency)
	- There is a script of a tensorflow model that stores a neural network, trained with Accelerometer data of the watch, which is then being loaded into the mainprogam
	- Visualization in streamlit that tells, whether the person carrying the watch is moving or is not, using the loaded NN
	- Visualization of the person's current skin temperature
	
Obviously, you cannot use this code in order to see the results of the data processing, since you probably do not have a E4 wrist watch.
Neither do I. This project was part of my timed job in the Signal and System Theory Group at the 
Department of Electrical Engineering & Information in the University of Paderborn.
If you want to see some screenshots of the main result in the local streamlit window feel free to email me: dennis.born@outlook.de
