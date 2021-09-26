'''

Adapted excerpt from Getting Started with Raspberry Pi by Matt Richardson

DHT 22 - GPIO 4
RELAY - GPIO 17

Modified by Rui Santos
Complete project details: http://randomnerdtutorials.com

'''

import RPi.GPIO as GPIO
import Adafruit_DHT
from flask import Flask, render_template, request
import datetime
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   17 : {'name' : 'heater', 'state' : GPIO.HIGH},
   # 24 : {'name' : 'GPIO 24', 'state' : GPIO.LOW}
   }

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.HIGH)

def getTimeString():
   now = datetime.datetime.now()
   return now.strftime("%Y-%m-%d %H:%M")

@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   timeString = getTimeString()
   humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'time' : timeString,
      'pins' : pins,
      'temp' : temperature,
      'hmty' : humidity
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.LOW)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.HIGH)
      message = "Turned " + deviceName + " off."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   timeString = getTimeString()
   humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'time' : timeString,
      'pins' : pins,
      'temp' : temperature,
      'hmty' : humidity
   }

   return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
