# Thermostat

Project uses a Raspberry Pi Zero W, 3.3 volt relay module, and a DHT22 temperature and humidity sensor

Relay module used: [link](https://www.aliexpress.com/item/4000480944773.html?spm=a2g0s.9042311.0.0.547c4c4dJpZ0KU)

## Raspberry Pi Zero W Setup

Install [Raspberry-pi imager](https://www.raspberrypi.org/software/)

> choco install rpi-imager

Open Raspberry Pi Imager program

Raspberry Pi OS (other) -> Raspberry Pi OS Lite

Ensure SD card is inserted and selected.

Select "Write"

Add a blank file named "ssh" with no extensions

Add [wpa_supplicant file](https://www.raspberrypi.org/documentation/computers/configuration.html#configuring-networking31). 

ssh into pi, change default password

```
sudo apt update
sudo apt upgrade
sudo apt-get install python3-pip python3-flask
sudo pip install flask
sudo python3 -m pip install --upgrade pip setuptools wheel
sudo pip3 install Adafruit_DHT
```

## Wiring

[raspberry pi pinout diagram](https://pinout.xyz/#)

![wiring diagram](/pi-zero-thermostat_bb.png)

| Signal Pins | |
| --- | --- |
| DHT 22 | GPIO 4 |
| RELAY | GPIO 17 |

<!-- | Raspberry Pi | Relay | 
| --- | --- | 
| ```3v3 Power``` | ```Vcc``` |
| ```Ground``` | ```Gnd``` |
| ```BCM 23``` | ```In1``` |

## How I modified the example code 

The example code is for controlling two LEDs using the GPIO pins. I modified the code to control a single relay

### Changes to app.py

All changes mades in the order at which they appear in the code

| # | Existing Code | After Modifications | Notes |
|---|---|---|---|
|1| ```23 : {'name' : 'GPIO 23', 'state' : GPIO.LOW}``` | ```23 : {'name' : 'GPIO 23', 'state' : GPIO.HIGH}``` | The relay is triggered by a connection between ```In1``` and ```Gnd```, therefore, the off state of the relay is triggered with a ```GPIO.HIGH``` output through pin ```23``` |
|2| ```24 : {'name' : 'GPIO 24', 'state' : GPIO.LOW}``` | ```# 24 : {'name' : 'GPIO 24', 'state' : GPIO.LOW}``` | pin ```24``` is not used, so it is commented out |
|3| ```GPIO.output(pin, GPIO.LOW)``` | ```GPIO.output(pin, GPIO.HIGH)``` | same reason as change #1 |
|4| ```GPIO.output(changePin, GPIO.HIGH)``` | ```GPIO.output(changePin, GPIO.LOW)``` | same reason as change #1. On state = ```GPIO.LOW```, off state = ```GPIO.HIGH``` |
|5| ```GPIO.output(changePin, GPIO.LOW)``` | ```GPIO.output(changePin, GPIO.HIGH)``` | Off state = ```GPIO.HIGH```, on state = ```GPIO.LOW```

### Changes to html.main

All changes mades in the order at which they appear in the code

| # | Existing Code | After Modifications | Notes |
|---|---|---|---|
|1| ```{% if pins[pin].state == true %}``` | ```{% if pins[pin].state == false %}``` | pin state must be reversed | -->
