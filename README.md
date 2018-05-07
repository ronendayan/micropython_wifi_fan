# micropython_wifi_fan
Turn a simple fan to wifi fan using micropython
---
For this project I used:
* Simple Fan
* Wemos D1 Mini
* 3x 1 channel relay module
* AC100~240V to 5V converter  

<img src="https://j.lnwfile.com/_/j/_raw/hs/my/fx.jpg" width="200" height="200" />
<img src="https://images-na.ssl-images-amazon.com/images/I/61IwgJRgiyL._SY355_.jpg" width="200" height="200" />
<img src="https://s-media-cache-ak0.pinimg.com/originals/10/6a/de/106ade153ee179a341795a57ca478db6.jpg" width="200" height="200" />


---
The fan:  
![alt text](https://github.com/ronendayan/micropython_wifi_fan/blob/master/pictures/IMG_20180507_082219.jpg "Fan")

Assemble the parts:  
### Step 1  
I connected the fan buttons directly to the wemos:
* Brown to GND
* Blue (Speed 1) to D1
* White (Speed 2) to D2
* Red (Speed 3) to D3

![alt text](https://github.com/ronendayan/micropython_wifi_fan/blob/master/pictures/IMG_20180505_083108.jpg "Buttons")
### Step 2
I connected the 220v power cable to all 3 relays (bridge them all togther) and also to the AC100~240V to 5V converter (To power up the wemos).  

Next, I connected the motor cables to the relays, one for each relay
* Blue to Relay 1
* White to Relay 2
* Red to Relay 3

And connect the relays to the wemos
* Relay 1 (Blue) to D5
* Relay 2 (White) to D6
* Relay 3 (Red) to D7

![alt text](https://github.com/ronendayan/micropython_wifi_fan/blob/master/pictures/IMG_20180505_083058.jpg "Relays")

### Step 3
Deploy the code:  
You will need to edit the file before deploy:  
For the MQTT settings
```python
CONFIG = {
"broker": b"<MQTT_SERVER>",
"username": b"<MQTT_USER>",
"password": b"<MQTT_PASSWORD>",
"client_id": b"wififan",
"cmd_topic": b"home/fan/set",
"state_topic": b"home/fan/state",
"speed_topic": b"home/fan/speed/state",
"speed_cmd_topic": b"home/fan/speed/set"
}
```
And for the WiFi
```python
def connect_to_home_wifi():
    print("Connecting to WiFi")
    sta_if.active(True)
    time.sleep(1)
    sta_if.connect('<WIFI_SSID>', '<WIFI_PASS>')
    time.sleep(1)
    print(sta_if.ifconfig())
```

---
All together:  

![alt text](https://github.com/ronendayan/micropython_wifi_fan/blob/master/pictures/IMG_20180505_083034.jpg "All_1")

![alt text](https://github.com/ronendayan/micropython_wifi_fan/blob/master/pictures/IMG_20180506_230617.jpg "All_2")

