#!/usr/bin/python

# monitor.py - For Terrarium Controllers using Adafruit
# DHT sensors, Energenie Pimote sockets, and ThingSpeak.
# MIT license.
# http://bennet.org/blog/raspberry-pi-terrarium-controller/

# Imports
import RPi.GPIO as GPIO
import Adafruit_DHT
import energenie
import requests

# Attempt to get a sensor reading. The read_retry method will
# retry up to 15 times, waiting 2 seconds between attempts
sensormodel = Adafruit_DHT.AM2302
sensorpin = 4
humidity, temperature = Adafruit_DHT.read_retry(sensormodel, sensorpin)

# If either reading has failed after repeated retries,
# abort and log message to ThingSpeak
thingspeak_key = 'XXXXXXXXXXXXXXXX'
if humidity is None or temperature is None:
	f = requests.post('https://api.thingspeak.com/update.json', data = {'api_key':thingspeak_key, 'status':'failed to get reading'})

# Otherwise, check if temperature is above threshold,
# and if so, activate Energenie socket for cooling fan
else:
	fansocket = 1
	tempthreshold = 28

	if temperature &gt; tempthreshold:
		# Activate cooling fans
		energenie.switch_on(fansocket)

	else:
		# Deactivate cooling fans
		energenie.switch_off(fansocket)

	# Send the data to Thingspeak
	r = requests.post('https://api.thingspeak.com/update.json', data = {'api_key':thingspeak_key, 'field1':temperature, 'field2':humidity})