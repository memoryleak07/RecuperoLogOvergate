import json
import os
import sys
import shutil
import subprocess
import time
from datetime import datetime
import tempfile

def validateDate():
    while True:
        try:
            date = input("[>>] Insert date in this format dd/mm/YYYY\n")
            datetime.strptime(date, '%d/%m/%Y')
            return date
        except ValueError:
            print("\n[X] You must insert date in this format dd/mm/YYYY", ValueError, "\n")


def dateRange(createddate, startdate, enddate):
    #determines if date is in range
    createddate = datetime.strptime(createddate, '%a %b %d %H:%M:%S %Y')
    startdate = datetime.strptime(startdate, '%d/%m/%Y')
    enddate = datetime.strptime(enddate, '%d/%m/%Y').replace(hour=23, minute=59, second=59)
    return startdate < createddate < enddate


def createTempDir():
    with tempfile.TemporaryDirectory(dir="C:\Ditron") as tmpdirname:
        print('created temporary directory', tmpdirname)

def getPvInfo():
    with open("m.json") as jsondata:
        data = json.load(jsondata)
        fil = data["filiali"]

    filiale = input("\n[+] Numero della filiale: \n")
    if filiale not in fil:
        raise ValueError("[X] Nessuna filiale trovata")
    print("\n", fil[filiale]["title"])
    filiale = fil[filiale]

    numerocassa = input("\n[+] Numero della cassa: \n")
    for val in fil[filiale]["cassa"]:
        if numerocassa not in fil[filiale]["cassa"]:
                raise ValueError("[X] Nessuna cassa trovata")
    print("\n", fil[filiale]["cassa"][numerocassa])
    return (r"\\" + (fil[filiale]["cassa"][numerocassa][0]))


def recuperoFile(dir):
    ovgpath= os.path.join(ip+dir)
    for filename in os.listdir(ovgpath):
        files = os.path.join(ovgpath+"\\"+filename)
        #print(files)
        created = time.ctime(os.path.getmtime(files))
        if dateRange(created, start, end):
            try:
                if dateRange(created, start, end):
                    shutil.copy2(files, temp.name)
                    print("[<<] File transferred " + filename + created, " ")
                else:
                    pass
                    #print("[+] File not transferred " + filename + created)
            except (os.error, Exception) as err:
                print("[X] File not transferred " + filename, err)
    print("\n[+] Transfer complete")



# createTempDir()
# with tempfile.TemporaryDirectory(dir="C:\Ditron") as tmpdirname:
#     print('created temporary directory', tmpdirname)

username = "ditronpos"
password = "sopnortid"
today = datetime.today().strftime('%Y%m%d%H%M%S')
maindir = r"C:\Ditron"
temp = tempfile.TemporaryDirectory(dir=maindir)

ip = getPvInfo()

cmd = 'NET USE ' + ip + ' /User:' + username + ' ' + password
subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

print("\n[+] Data inizio: ") 
start = validateDate()

print("\n[+] Data fine: ") 
end = validateDate()

print("\n[+] Recupero PPOS/run: ") 
dir = r"\c-drive\PPOS\RUN"
recuperoFile(dir)

print("\n[+] Recupero Overgate log: ") 
dir = r"\c-drive"
recuperoFile(dir)

print("\n[+] Recupero FiscalPrinter log: ") 
dir = r"\c-drive\Log\DitronRT"
recuperoFile(dir)


if len(os.listdir(temp.name)) == 0:
    input("\n[X] NOT OK! Some errors occured during the process\n[>] Press any key to exit program: \n")
    sys.exit() 
else:
    print("\n[+] Zipping files .. ")
    zipfile = "fil" + today
    zip = shutil.make_archive(os.path.join(maindir, zipfile), 'zip', temp.name)
    print("\n[+] Zip file is: \n\n"+ zip)
    input("\n[+] OK! Job done!\n[>] Press any key to exit program: \n")

