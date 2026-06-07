import os
import signal
from configparser import ConfigParser
from pythonosc.udp_client import SimpleUDPClient as UDPClient
from gpiozero import Button

#Checks for valid config file
if os.path.isfile("config.ini"):
    print(f"Found valid config at: \"{os.path.abspath('config.ini')}\"")
else:
    config = ConfigParser()
    config['Config'] = {'log': '0', 'ip': '192.168.0.2', 'port': 8500, 'bounce': 0, 'PGM1_pin': 26,
                                 'PGM2_pin': 19, 'PGM3_pin': 16,
                                 'PGM4_pin': 20, 'PGM5_pin': 0, 'PGM6_pin': 0, 'PGM7_pin': 0, 'PGM8_pin': 0,
                                 'PGM9_pin': 0, 'PGM10_pin': 0}
    with open("config.ini", "w", encoding="utf-8") as configfile:
        print("Config file not found. Creating standard config")
        config.write(configfile)
        print(f"Config file created at: \"{os.path.abspath('config.ini')}\"")

#Import and read the config file
Config = ConfigParser()
Config.read("config.ini")

ip = Config.get('Config', 'ip')
log = Config.getboolean('Config', 'log')
bounce = Config.getfloat('Config', 'bounce')
port = Config.getint('Config', 'port')
PGM1 = Config.getint('Config', 'PGM1_pin')
PGM2 = Config.getint('Config', 'PGM2_pin')
PGM3 = Config.getint('Config', 'PGM3_pin')
PGM4 = Config.getint('Config', 'PGM4_pin')
PGM5 = Config.getint('Config', 'PGM5_pin')
PGM6 = Config.getint('Config', 'PGM6_pin')
PGM7 = Config.getint('Config', 'PGM7_pin')
PGM8 = Config.getint('Config', 'PGM8_pin')
PGM9 = Config.getint('Config', 'PGM9_pin')
PGM10 = Config.getint('Config', 'PGM10_pin')

client = UDPClient(ip, port)
print(f"UDPClient will connect to |IP: {ip}| |Port: {port}|")

#Setup GPIO pins if they're defined
if PGM1 != 0:
    pgm1 = Button(PGM1, bounce_time=bounce)
if PGM2 != 0:
    pgm2 = Button(PGM2, bounce_time=bounce)
if PGM3 != 0:
    pgm3 = Button(PGM3, bounce_time=bounce)
if PGM4 != 0:
    pgm4 = Button(PGM4, bounce_time=bounce)
if PGM5 != 0:
    pgm5 = Button(PGM5, bounce_time=bounce)
if PGM6 != 0:
    pgm6 = Button(PGM6, bounce_time=bounce)
if PGM7 != 0:
    pgm7 = Button(PGM7, bounce_time=bounce)
if PGM8 != 0:
    pgm8 = Button(PGM8, bounce_time=bounce)
if PGM9 != 0:
    pgm9 = Button(PGM9, bounce_time=bounce)
if PGM10 != 0:
    pgm10 = Button(PGM10, bounce_time=bounce)


#Encodes tally data as OSC Protocol
def osc_builder(address: int, state: str):
    if not (1 <= address <= 255):
        raise ValueError("Address must be between 1 and 255")
    if state == "PGM_on":
        tally = "/tally/program_on"
    elif state == "PGM_off":
        tally = "/tally/program_off"
    else:
        tally = "/tally/previewprogram_off"
    if log:
        print(f"Commando for Tally Arbiter | Address: {address} & Msg: {tally}")
    client.send_message(tally, address)


def pgm_onadd(x):
    def PGM_on(pin = x):
        osc_builder(pin, "PGM_on")
        if log:
            print(f"OSC message sent to |IP: {ip} & Port: {port}|")
            print("________________________________________\n")
    return PGM_on

def pgm_offadd(x):
    def PGM_off(pin = x):
        osc_builder(pin, "PGM_off")
        if log:
            print(f"OSC message sent to |IP: {ip} & Port: {port}|")
            print("________________________________________\n")
    return PGM_off


#GPIO event handler
if PGM1 != 0:
    pgm1.when_pressed = pgm_onadd(1)
    pgm1.when_released = pgm_offadd(1)
if PGM2 != 0:
    pgm2.when_pressed = pgm_onadd(2)
    pgm2.when_released = pgm_offadd(2)
if PGM3 != 0:
    pgm3.when_pressed = pgm_onadd(3)
    pgm3.when_released = pgm_offadd(3)
if PGM4 != 0:
    pgm4.when_pressed = pgm_onadd(4)
    pgm4.when_released = pgm_offadd(4)
if PGM5 != 0:
    pgm5.when_pressed = pgm_onadd(5)
    pgm5.when_released = pgm_offadd(5)
if PGM6 != 0:
    pgm6.when_pressed = pgm_onadd(6)
    pgm6.when_released = pgm_offadd(6)
if PGM7 != 0:
    pgm7.when_pressed = pgm_onadd(7)
    pgm7.when_released = pgm_offadd(7)
if PGM8 != 0:
    pgm8.when_pressed = pgm_onadd(8)
    pgm8.when_released = pgm_offadd(8)
if PGM9 != 0:
    pgm9.when_pressed = pgm_onadd(9)
    pgm9.when_released = pgm_offadd(9)
if PGM9 != 0:
    pgm10.when_pressed = pgm_onadd(10)
    pgm10.when_released = pgm_offadd(10)


print("Program started. Use CTRL + C to exit")
signal.pause()
