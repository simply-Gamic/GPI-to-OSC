import os
from signal import pause
from gpiozero import Button
from configparser import ConfigParser
from pythonosc.udp_client import SimpleUDPClient as UDPClient

#Checks for valid config file
if os.path.isfile("config.ini"):
    print(f"Found valid config at: \"{os.path.abspath('config.ini')}\"")
else:
    with open("config.ini", "w", encoding="utf-8") as f:
        print("Config file not found. Creating standard config")
        f.write(f"""[Config]\nlog = 0\nip = 192.0.0.2\nport = 8500\nPRV1_pin = 26\nPGM1_pin = 19\nPRV2_pin = 16\nPGM2_pin = 20""")
        print(f"Config file created at: \"{os.path.abspath('config.ini')}\"")

#Import and read the config file
Config = ConfigParser()
Config.read("config.ini")
log = Config['Config']['log']
ip = Config['Config']['ip']
port = int(Config['Config']['port'])
PGM1 = int(Config['Config']['PGM1_pin'])
PGM2 = int(Config['Config']['PGM2_pin'])
PRV1 = int(Config['Config']['PRV1_pin'])
PRV2 = int(Config['Config']['PRV2_pin'])

client = UDPClient(ip, port)
print(f"UDPClient will connect to |IP: {ip}| |Port: {port}|")

# Setup GPIO pins
pgm1 = Button(PGM1)
pgm2 = Button(PGM2)
prv1 = Button(PRV1)
prv2 = Button(PRV2)


#Encodes tally data as OSC Protocol and sends it to TallyArbiter
def osc_builder(address: int, state: str):
    if not (1 <= address <= 255):
        raise ValueError("Address must be between 1 and 255")
    if state == "PRV_on":
        tally = "/tally/preview_on"
    elif state == "PRV_off":
        tally = "/tally/preview_off"
    elif state == "PGM_on":
        tally = "/tally/program_on"
    elif state == "PGM_off":
        tally = "/tally/program_off"
    else:
        tally = "/tally/previewprogram_off"
    client.send_message(tally, address)
    if log == "1":
        print(f"Commando for Tally Arbiter | Address:{address} & Msg: {tally}")


def pgm_onadd(x):
    def pgm_on(pin = x):
        osc_builder(pin, "PGM_on")
    return pgm_on

def pgm_offadd(x):
    def pgm_off(pin = x):
        osc_builder(pin, "PGM_off")
    return pgm_off

def prv_onadd(x):
    def prv_on(pin = x):
        osc_builder(pin, "PRV_on")
    return prv_on

def prv_offadd(x):
    def prv_off(pin = x):
        osc_builder(pin, "PRV_off")
    return prv_off


#GPIO event handler
if PGM1 != 0:
    pgm1.when_pressed = pgm_onadd(1)
    pgm1.when_released = pgm_offadd(1)
if PGM2 != 0:
    pgm2.when_pressed = pgm_onadd(2)
    pgm2.when_released = pgm_offadd(2)
if PRV1 != 0:
    prv1.when_pressed = prv_onadd(3)
    prv1.when_released = prv_offadd(3)
if PRV2 != 0:
    prv2.when_pressed = prv_onadd(4)
    prv2.when_released = prv_offadd(4)


print("Program started. Use CTRL + C to exit")
pause()
