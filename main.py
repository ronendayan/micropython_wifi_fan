import os
import time
import network
import utime
import machine
import ubinascii
import webrepl
from umqtt.simple import MQTTClient
from machine import Pin


def connect_to_home_wifi():
    print("Connecting to WiFi")
    sta_if.active(True)
    time.sleep(1)
    sta_if.connect('<WIFI_SSID>', '<WIFI_PASS>')
    time.sleep(1)
    print(sta_if.ifconfig())


def load_config():
    import ujson as json
    try:
        with open("/config.json") as f:
            config = json.loads(f.read())
    except (OSError, ValueError):
        print("Couldn't load /config.json")
        save_config()
    else:
        CONFIG.update(config)
        print("Loaded config from /config.json")


def save_config():
    import ujson as json
    try:
        with open("/config.json", "w") as f:
            f.write(json.dumps(CONFIG))
    except OSError:
        print("Couldn't save /config.json")


def connect_to_mqtt():
    print("Connecting to MQTT broker")
    client = MQTTClient(CONFIG['client_id'], CONFIG['broker'], user=CONFIG['username'], password=CONFIG['password'])
    try:
        client.connect()
        print("Connected to {}".format(CONFIG['broker']))
        return client
    except:
        print("Failed to connect to MQTT, retrying...")
        return None


def sub_speed_cb(topic, msg):
    print((topic, msg))
    if msg == b"low":
        turn_off(level_one)
        turn_off(level_two)
        turn_off(level_three)
        turn_on(1)
    elif msg == b"medium":
        turn_off(level_one)
        turn_off(level_two)
        turn_off(level_three)
        turn_on(2)
    elif msg == b"high":
        turn_off(level_one)
        turn_off(level_two)
        turn_off(level_three)
        turn_on(3)

def sub_cb(topic, msg):
    print((topic, msg))

    if topic == b'home/fan/set':
        print('Got home/fan/set')
        if msg == b"off":
            turn_on(0)
        elif msg == b"on":
            turn_on(1)

    elif topic == b'home/fan/speed/set':
        print('Got home/fan/speed/set')
        if msg == b"low":
            turn_on(1)
        elif msg == b"medium":
            turn_on(2)
        elif msg == b"high":
            turn_on(3)


def publish_msg(msg):
    print("Got order to pub for: {}".format(msg))
    # return
    try:
        if msg == 1:
            state_msg = 'on'
            speed_msg = 'low'
            print('Going to publish: topic: {}, state: {}, speed: {}'.format(CONFIG['state_topic'], state_msg, speed_msg))
            c.publish(CONFIG['state_topic'], bytes(str(state_msg), 'utf-8'))
            c.publish(CONFIG['speed_topic'], bytes(str(speed_msg), 'utf-8'))
        elif msg == 2:
            state_msg = 'on'
            speed_msg = 'medium'
            print('Going to publish: state: {}, speed: {}'.format(state_msg, speed_msg))
            c.publish(CONFIG['state_topic'], bytes(str(state_msg), 'utf-8'))
            c.publish(CONFIG['speed_topic'], bytes(str(speed_msg), 'utf-8'))
        elif msg == 3:
            state_msg = 'on'
            speed_msg = 'high'
            print('Going to publish: state: {}, speed: {}'.format(state_msg, speed_msg))
            c.publish(CONFIG['state_topic'], bytes(str(state_msg), 'utf-8'))
            c.publish(CONFIG['speed_topic'], bytes(str(speed_msg), 'utf-8'))
        elif msg == 0:
            state_msg = 'off'
            print('Going to publish: topic: {}, state: {}'.format(CONFIG['state_topic'], state_msg))
            c.publish(CONFIG['state_topic'], bytes(str(state_msg), 'utf-8'))
        
        
    except Exception as e:
        print("Failed to publish: {}".format(CONFIG['state_topic']))
        print(e)


def turn_off(fan_speed):
    fan_speed(1)


def turn_on(fan_speed):

    turn_off(level_one)
    turn_off(level_two)
    turn_off(level_three)

    if fan_speed == 1:
        level_one(0)
        
    elif fan_speed == 2:
        level_two(0)
        
    elif fan_speed == 3:
        level_three(0)
        
    elif fan_speed == 0:
        print('0')

    publish_msg(fan_speed)
        
    
def main():

    global btn_state, fan_state, c

    c = connect_to_mqtt()
    while not c:
        time.sleep(2)
        c = connect_to_mqtt()

    c.set_callback(sub_cb)

    c.subscribe(CONFIG['cmd_topic'])
    c.subscribe(CONFIG['speed_cmd_topic'])
    print("Connected to %s, subscribed to %s topic" % (CONFIG['broker'], CONFIG['cmd_topic']))
    print("Connected to %s, subscribed to %s topic" % (CONFIG['broker'], CONFIG['speed_cmd_topic']))
    turn_on(0)
    try:
        while True:

            time.sleep(0.01)
        
            print('-------------------------------------------')
            print('button_one_first: {}'.format(button_one.value()))
            print('button_two_first: {}'.format(button_two.value()))
            print('button_three_first: {}'.format(button_three.value()))
            print('-------------------------------------------')

            cur_btn = 0

            if not button_one.value():
                cur_btn = 1
            elif not button_two.value():
                cur_btn = 2
            elif not button_three.value():
                cur_btn = 3
            else:
                cur_btn = 0
            
            if cur_btn != btn_state:
                print('enter here')
                btn_state = cur_btn
                turn_on(cur_btn)

            c.check_msg()

    finally:
        c.disconnect()


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


sta_if = network.WLAN(network.STA_IF)

#pin 14 = D5
level_one = Pin(14, Pin.OPEN_DRAIN)
level_one(1)
#pin 12 = D6
level_two = Pin(12, Pin.OPEN_DRAIN)
level_two(1)
#pin 13 = D7
level_three = Pin(13, Pin.OPEN_DRAIN)
level_three(1)
# pin 5 - D1
button_one = Pin(5, Pin.IN, Pin.PULL_UP)
# pin 4 - D2
button_two = Pin(4, Pin.IN, Pin.PULL_UP)
# pin 0 - D3
button_three = Pin(0, Pin.IN, Pin.PULL_UP)

client = None
state = 0

btn_state = 0
fan_state = 0

if __name__ == '__main__':
    load_config()
    connect_to_home_wifi()
    main()

