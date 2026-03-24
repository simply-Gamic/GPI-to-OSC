import os
import signal
from configparser import ConfigParser
from pythonosc.udp_client import SimpleUDPClient as UDPClient
from gpiozero import Button

#Checks for valid config file
if os.path.isfile("config.ini"):
    print(f"Found valid config at: \"{os.path.abspath('config.ini')}\"")
else:
    with open("config.ini", "w", encoding="utf-8") as f:
        print("Config file not found. Creating standard config")
        f.write(f"""[Config]\nlog = 0\nip = 192.168.0.2\nport = 8500\nPGM1_pin = 26\nPGM2_pin = 19\nPGM3_pin = 16\n
        PGM4_pin = 20\nPGM5_pin = 0\nPGM6_pin = 0\nPGM7_pin = 0\nPGM8_pin = 0\nPGM9_pin = 0\nPGM10_pin = 0""")
        print(f"Config file created at: \"{os.path.abspath('config.ini')}\"")

#Import and read the config file
Config = ConfigParser()
Config.read("config.ini")
log = Config['Config']['log']
ip = Config['Config']['ip']
port = int(Config['Config']['port'])
PGM1 = int(Config['Config']['PGM1_pin'])
PGM2 = int(Config['Config']['PGM2_pin'])
PGM3 = int(Config['Config']['PGM3_pin'])
PGM4 = int(Config['Config']['PGM4_pin'])
PGM5 = int(Config['Config']['PGM5_pin'])
PGM6 = int(Config['Config']['PGM6_pin'])
PGM7 = int(Config['Config']['PGM7_pin'])
PGM8 = int(Config['Config']['PGM8_pin'])
PGM9 = int(Config['Config']['PGM9_pin'])
PGM10 = int(Config['Config']['PGM10_pin'])

client = UDPClient(ip, port)
print(f"UDPClient will connect to |IP: {ip}| |Port: {port}|")

#Setup GPIO pins if they're defined
if PGM1 != 0:
    pgm1 = Button(PGM1)
if PGM2 != 0:
    pgm2 = Button(PGM2)
if PGM3 != 0:
    pgm3 = Button(PGM3)
if PGM4 != 0:
    pgm4 = Button(PGM4)
if PGM5 != 0:
    pgm5 = Button(PGM5)
if PGM6 != 0:
    pgm6 = Button(PGM6)
if PGM7 != 0:
    pgm7 = Button(PGM7)
if PGM8 != 0:
    pgm8 = Button(PGM8)
if PGM9 != 0:
    pgm9 = Button(PGM9)
if PGM10 != 0:
    pgm10 = Button(PGM10)


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
    if log == "1":
        print(f"Commando for Tally Arbiter | Address: {address} & Msg: {tally}")
    client.send_message(tally, address)


def pgm_onadd(x):
    def PGM_on(pin = x):
        osc_builder(pin, "PGM_on")
        if log == "1":
            print(f"OSC message sent to |IP: {ip} & Port: {port}|")
            print("________________________________________\n")
    return PGM_on

def pgm_offadd(x):
    def PGM_off(pin = x):
        osc_builder(pin, "PGM_off")
        if log == "1":
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
