#!/usr/bin/python3
# File: wifi.py
# Author: bgstack15
# Startdate: 2016-11-03
# Title: Script that Connects to Wifi Using a Config File
# Package: wifi
# Purpose: To store wireless network settings and also use them
# History:
# Usage:
# Reference:
#    get command output http://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output/13135985#13135985
#     also http://stackoverflow.com/questions/606191/convert-bytes-to-a-python-string#606199
#    man nmcli
# Improve:
#    specify connection name or filename
#    provide --verbose flag

import re, subprocess

wifipyversion = "2016-11-03b"

# DEFINE FUNCTIONS
def _run_command(command):
   # reference: http://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output/13135985#13135985
   p = subprocess.Popen(command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
   return iter(p.stdout.readline, b'')

def run_command(command):
   rc_out = []
   for line in _run_command(command.split()):
      rc_out.append(line.decode("utf-8").rstrip())
   return rc_out

def getwnic():
   getwnic = ""
   for line in run_command('iw dev'):
      if "Interface" in line:
         getwnic = line.split()[1]
   return getwnic

def getvaluefromfile(filename, searchstring):
   # looks for "searchstring=" and then returns whatever is after that on that line, in filename
   thisvalue = ""
   filename = re.sub("^file://", "", filename)
   try:
      for line in open(filename, 'r'):
         line = line.strip()
         if re.compile(searchstring + "=").match(line):
            thisvalue = re.sub("^" + searchstring + "=", "", line)
         
   except Exception as e:
      print("Fatal error opening file: " + filename)
      quit()

   return thisvalue

# SAMPLE VARIABLES
configfile = "/home/bgstack15-local/software/wifi/campus.wifi"
conname = "" # gets con-name
nmcli_con_add = [] # gets type, ifname, con-name, ssid
nmcli_con_mod = [] # gets everything else

# PARSE CONFIG FILE
for line in open(configfile):
   usedline=0
   line = re.sub('#.*', '', line).rstrip()
   if line != "":
      #print(line)
      words = line.split()
      if "type" in words[0] or "ifname" in words[0] or "con-name" in words[0] \
               or "ssid" in words[0]:
         if "$WNIC" in words[1]:
            words[1] = str(getwnic())
         nmcli_con_add.append(words[0] + " " + words[1])
         usedline=1
         if "con-name" in words[0]:
            conname = words[1]
      else:
         # everything else goes to nmcli_con_mod
         if "identity" in words[0]:
            if "file:///" in words[1]:
               nmcli_con_mod.append(words[0] + " " + getvaluefromfile(words[1],"username"))
               usedline = 1
         elif "password" in words[0]:
            if "file:///" in words[1]:
               nmcli_con_mod.append(words[0] + " " + getvaluefromfile(words[1],"password"))
               usedline = 1
         if usedline != 1:
            nmcli_con_mod.append(words[0] + " " + words[1])

# DEBUG
if False:
   print("nmcli_con_add: " + str(nmcli_con_add))
   print("conname: " + conname)
   print("nmcli_con_mod: " + str(nmcli_con_mod))

# DELETE EXISTING CONNAME if exists
nmcondel = "nmcli con del " + conname
print(nmcondel)
run_command(nmcondel)

# EXECUTE NMCLI CON ADD
nmconadd = "nmcli con add"
for thisstring in nmcli_con_add:
   nmconadd = nmconadd + " " + thisstring
print(nmconadd)
run_command(nmconadd)

# EXECUTE NMCLI CON MODIFY
nmconmod = "nmcli con modify " + conname
nmconmodprint = "nmcli con modify " + conname
for thisstring in nmcli_con_mod:
   nmconmod = nmconmod + " " + thisstring
   nmconmodprint = nmconmodprint + " " + re.sub("(password ).*","\\1REDACTED", thisstring)
print(nmconmodprint)
run_command(nmconmod)

# EXECUTE NMCLI CON UP
nmconup = "nmcli con up " + conname
print(nmconup)
run_command(nmconup)
