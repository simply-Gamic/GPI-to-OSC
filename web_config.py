import os
import sys
import time
import socket
import urllib.parse
import subprocess
from configparser import ConfigParser
from http.server import BaseHTTPRequestHandler, HTTPServer

#Checks for valid config file
if os.path.isfile("config.ini"):
    print(f"Found valid config at: \"{os.path.abspath('config.ini')}\"")
else:
    with open("config.ini", "w", encoding="utf-8") as f:
        print("Config file not found. Creating standard config")
        f.write(f"""[Config]\nlog = 0\nip = 192.168.0.2\nport = 8500\nPGM1_pin = 26\nPGM2_pin = 19\nPGM3_pin = 16\nPGM4_pin = 20\nPGM5_pin = 0\nPGM6_pin = 0\nPGM7_pin = 0\nPGM8_pin = 0\nPGM9_pin = 0\nPGM10_pin = 0""")
        print(f"Config file created at: \"{os.path.abspath('config.ini')}\"")

#Import and read the config file
Config = ConfigParser()
Config.read("config.ini")
logc = Config['Config']['log']
ipc = Config['Config']['ip']
portc = int(Config['Config']['port'])
PGM1c = int(Config['Config']['PGM1_pin'])
PGM2c = int(Config['Config']['PGM2_pin'])
PGM3c = int(Config['Config']['PGM3_pin'])
PGM4c = int(Config['Config']['PGM4_pin'])
PGM5c = int(Config['Config']['PGM5_pin'])
PGM6c = int(Config['Config']['PGM6_pin'])
PGM7c = int(Config['Config']['PGM7_pin'])
PGM8c = int(Config['Config']['PGM8_pin'])
PGM9c = int(Config['Config']['PGM9_pin'])
PGM10c = int(Config['Config']['PGM10_pin'])


#Handles automatic restart after config change
def restart():
   try:
      #Check if running as root
      if os.geteuid() != 0:
         print("Error: This script must be run as root (use sudo)")
         sys.exit(1)
      print("Restarting RaspPi...")
      subprocess.run(["sudo", "reboot"], check=True)

   except subprocess.CalledProcessError as e:
      print(f"Failed to restart RasPi: {e}")
   except Exception as e:
      print(f"Unexpected error: {e}")


#Handles the webserver requests
class LocalFormHandler(BaseHTTPRequestHandler):
   def do_GET(self):
      self.send_response(200)
      self.send_header("Content-type", "text/html")
      self.end_headers()
      #HTML hardcoded for now instead of premade files
      page_content = f"""<html><body style='font-family:Arial; background:#f2f2f2; color:#333;'>
      <h2 style='color:#2c3e50;'>TallyGPI Config</h2>
      <form method='POST' style='margin-top:20px;'>
      <h3 style='color:#2c3150;'>Basic Configuration:</h3>
      TallyArbiter-IP: <input name='ip' type='text' placeholder='{ipc}' value='{ipc}' required style='padding:5px;'><br><br>
      TallyArbiter-Port: <input name='port' type='number' placeholder='{portc}' value='{portc}' required min='1' max='99999' style='padding:5px;'><br><br>
      <h3 style='color:#2c3150;'>GPI pin assignment:</h3>
      <a href="https://raspberrypi.stackexchange.com/questions/12966/what-is-the-difference-between-board-and-bcm-for-gpio-pin-numbering" target="_blank" rel="noopener noreferrer">Beware of the board numbering vs BCM numbering scheme!</a><br><br>
      PGM1: <input name='PGM1' type='number' placeholder='{PGM1c}' value='{PGM1c}' required min='0' max='30' style='padding:5px;'><br><br>
      PGM2: <input name='PGM2' type='number' placeholder='{PGM2c}' value='{PGM2c}' required min='0' max='30' style='padding:5px;'><br><br>
      PGM3: <input name='PGM3' type='number' placeholder='{PGM3c}' value='{PGM3c}' required min='0' max='30' style='padding:5px;'><br><br>
      PGM4: <input name='PGM4' type='number' placeholder='{PGM4c}' value='{PGM4c}' required min='0' max='30' style='padding:5px;'><br><br>
      PGM5: <input name='PGM5' type='number' placeholder='{PGM5c}' value='{PGM5c}' required min='0' max='30' style='padding:5px;'><br><br>
      PGM6: <input name='PGM6' type='number' placeholder='{PGM6c}' value='{PGM6c}' required min='0' max='30' style='padding:5px;'><br><br>
      PGM7: <input name='PGM7' type='number' placeholder='{PGM7c}' value='{PGM7c}' required min='0' max='30' style='padding:5px;'><br><br>
      PGM8: <input name='PGM8' type='number' placeholder='{PGM8c}' value='{PGM8c}' required min='0' max='30' style='padding:5px;'><br><br>
      PGM9: <input name='PGM9' type='number' placeholder='{PGM9c}' value='{PGM9c}' required min='0' max='30' style='padding:5px;'><br><br>
      PGM10: <input name='PGM10' type='number' placeholder='{PGM10c}' value='{PGM10c}' required min='0' max='30' style='padding:5px;'><br><br>
      <h3 style='color:#2c3150;'>Create logs for sent messages?</h3>
      Yes: <input name='log' type='radio' value='1' required>
      No: <input name='log' type='radio' value='0'required checked><br><br>
      <input type='submit' value='Save' style='padding:5px 10px; background:#349800; color:white; border:none; cursor:pointer;'>
      <input type='reset' value='Reset to last values' style='padding:5px 10px; background:#3498db; color:white; border:none; cursor:pointer;'>
      </form></body></html>"""
      self.wfile.write(page_content.encode('utf-8'))


   #Handles the form submit and writes the new config to the file
   def do_POST(self):
      content_length = int(self.headers.get('Content-Length', 0))
      post_data = self.rfile.read(content_length)
      fields = urllib.parse.parse_qs(post_data.decode("utf-8"))
      log = fields.get("log", [""])[0]
      ip = fields.get("ip", [""])[0]
      port = fields.get("port", [""])[0]
      PGM1 = fields.get("PGM1", [""])[0]
      PGM2 = fields.get("PGM2", [""])[0]
      PGM3 = fields.get("PGM3", [""])[0]
      PGM4 = fields.get("PGM4", [""])[0]
      PGM5 = fields.get("PGM5", [""])[0]
      PGM6 = fields.get("PGM6", [""])[0]
      PGM7 = fields.get("PGM7", [""])[0]
      PGM8 = fields.get("PGM8", [""])[0]
      PGM9 = fields.get("PGM9", [""])[0]
      PGM10 = fields.get("PGM10", [""])[0]

      self.send_response(200)
      self.end_headers()

      #Check if anything on the config was changed and if yes write to file + restart
      if content_length != 33:
         with open("config.ini", "w", encoding="utf-8") as f:
            f.write(f"""[Config]\nlog = {log}\nip = {ip}\nport = {port}\nPGM1_pin = {PGM1}\nPGM2_pin = {PGM2}\nPGM3_pin = {PGM3}\nPGM4_pin = {PGM4}\nPGM5_pin = {PGM5}\nPGM6_pin = {PGM6}\nPGM7_pin = {PGM7}\nPGM8_pin = {PGM8}\nPGM9_pin = {PGM9}\nPGM10_pin = {PGM10}""")
         self.wfile.write(b"""<html><body style='font-family:Arial; background:#f2f2f2; color:#333;'>
         <h2 style='color:#2c3e50;'>Config</h2><h3 style='color:green;'>Config saved! RasPi will restart automatically in 10sec.</h3></body></html>""")
         time.sleep(10)
         restart()
      else:
         self.wfile.write(b"""<html><body style='font-family:Arial; background:#f2f2f2; color:#333;'>
         <h2 style='color:#2c3e50;'>Config</h2><h3 style='color:yellow;'>No configs changed! Reopen webpage to change settings if needed!</h3></body></html>""")


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()
server = HTTPServer((ip, 8000), LocalFormHandler)
server.serve_forever()
