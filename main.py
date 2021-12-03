import os
import sys
import shutil
import subprocess
import time
from datetime import datetime
import tempfile
import ftplib
import json
from json.decoder import JSONDecodeError

# Progress bar
# def trasferisciFTP(dir, filename):
#     from tqdm import tqdm
#     try:
#         #session = ftplib.FTP('pos.ditronetwork.com',"ditronetwork","Kr0wteN0rt!d")
#         session = ftplib.FTP('10.10.10.244',"ditronetwork","Kr0wteN0rt!d")
#         session.cwd("Retail/temp")
#         filesize = os.path.getsize(dir)
#         with open(dir, "rb") as file:
#             #session.storbinary('STOR {}'.format(filename), file) # send the file
#             with tqdm(unit = 'blocks', unit_scale = True, leave = False, miniters = 1, desc = 'Uploading...', total = filesize) as tqdm_instance:
#                 res = session.storbinary('STOR {}'.format(filename), file, 2048, callback = lambda sent: tqdm_instance.update(len(sent)))
#                 print(str(res))
#         session.quit()
#         return True
#     except ftplib.all_errors as err:
#         print (err)
#         return False

def renameTempDir(tempname, nomefile, maindir):
    os.rename(tempname, nomefile)
    shutil.move(nomefile, os.path.join(maindir, nomefile))
    print("Cartella temporanea rinominata: ", os.path.join(maindir, nomefile))


def userInput(param):
    userinput = input(param).lower()
    while str(userinput) != "x" and str(userinput) != "y" and str(userinput) != "":
        print("\n[-] You must enter Y or X!\n")
        userinput = input(param).lower()
    if str(userinput) == "x":
        return False
    if str(userinput) == "y" or str(userinput) == "":
        return True


def validateDate():
    while True:
        try:
            date = input("[>>] Insert date in this format dd/mm/YYYY: \n")
            datetime.strptime(date, '%d/%m/%Y')
            return date
        except ValueError:
            print("\n[X] You must insert date in this format dd/mm/YYYY!", ValueError, "\n")


def downloadUPDFile():
    try:
        cwd = os.getcwd()
        #session = ftplib.FTP('10.10.10.244',"ditronetwork","Kr0wteN0rt!d")
        session = ftplib.FTP('pos.ditronetwork.com',"ditronetwork","Kr0wteN0rt!d")
        session.cwd("Retail/temp")
        filenames = session.nlst()
        os.chdir(maindir)
        for filename in filenames:
            #if filename.startswith("UPD"):
            if filename.startswith("fil"):
                print("[+] File found: ", filename)
                try:
                    with open(filename, 'wb') as file :
                        res = session.retrbinary('RETR %s' % filename, file.write)
                        print("[<<]", str(res), "in", maindir)
                        file.close()
                except Exception as err:
                    print("Failed to download file", err)
            else:
                print("Filename not match:", filename)
        os.chdir(cwd)
    except ftplib.all_errors as err:
        print (err)


def trasferisciFTP(dir, filename):
    try:
        session = ftplib.FTP('pos.ditronetwork.com',"ditronetwork","Kr0wteN0rt!d")
        #session = ftplib.FTP('10.10.10.244',"ditronetwork","Kr0wteN0rt!d")
        session.cwd("Retail/temp")
        with open(dir, "rb") as file:
            res = session.storbinary('STOR {}'.format(filename), file) # send the file
            print("[<<]", str(res))
        session.quit()
        return True
    except ftplib.all_errors as err:
        print (err)
        return False



def getPvInfo():
    #Ritorna una tupla con IP della cassa e numero della filiale
    with open("m.json") as jsondata:
        try:
            data = json.load(jsondata)
            fil = data["filiali"]
            filiale = input("\n[+] Numero della filiale: \n")
            if filiale not in fil:
                raise ValueError("[X] Nessuna filiale trovata")
            numerofiliale = filiale
            filiale = fil[filiale]
            titolofiliale = filiale["title"]
            print("[+]\nFiliale numero: ", numerofiliale, "\nTitolo: ", titolofiliale)

            numerocassa = input("\n[+] Numero della cassa: \n")
            for val in (filiale["cassa"]):
                if numerocassa not in filiale["cassa"]:
                        raise ValueError("[X] Nessuna cassa trovata")

            ip = r"\\" + (filiale["cassa"][numerocassa][0])
            print("[+]\nIndirizzo cassa:", ip)

            return(ip, numerofiliale)

        except (ValueError, Exception, JSONDecodeError) as err:
            print("[X] JSON file is not valid:", err)
            return False


def dateRange(createddate, startdate, enddate):
    #Ritorna True se si trova nel range di date
    createddate = datetime.strptime(createddate, '%a %b %d %H:%M:%S %Y')
    startdate = datetime.strptime(startdate, '%d/%m/%Y')
    enddate = datetime.strptime(enddate, '%d/%m/%Y').replace(hour=23, minute=59, second=59)
    return startdate < createddate < enddate


def recuperoPPOS(dir):
    ovgpath= os.path.join(ip+dir)
    for filename in os.listdir(ovgpath):
        files = os.path.join(ovgpath+"\\"+filename)
        created = time.ctime(os.path.getmtime(files))
        if dateRange(created, start, end):
            try:
                shutil.copy2(files, temp.name)
                print("[<<] File transferred " + filename + created, " ")
            except (os.error, Exception) as err:
                print("[X] File not transferred " + filename, err)
        else:
            pass
            #print("[+] File not transferred " + filename + created)
    print("[+] Task complete")


def recuperoFile(dir, name, ext):
    ovgpath= os.path.join(ip+dir)
    for filename in os.listdir(ovgpath):
        files = os.path.join(ovgpath+"\\"+filename)
        created = time.ctime(os.path.getmtime(files))
        if dateRange(created, start, end) and filename.startswith(name) and filename.endswith(ext):
            try:
                shutil.copy2(files, temp.name)
                print("[<<] File transferred " + filename + created, " ")
            except (os.error, Exception) as err:
                print("[X] File not transferred " + filename, err)
        else:
            pass
    print("[+] Task complete")


def connectToSharedFolder(ip):
    pathtodrive = os.path.join(ip, "c-drive")
    print("\n[+] Provo ad accedere a:", pathtodrive, "...")

    cmd = 'NET USE ' + pathtodrive + ' /User:' + "ditronpos" + ' ' + "sopnortid"
    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    if os.path.exists(pathtodrive):
        print("[+] Il percorso esiste!")
        return True
    else:
        print("[X] Il percorso non esiste!")
        return False


if __name__ == "__main__":

    maindir = r"C:\Ditron"
    today = datetime.today().strftime('%Y%m%d%H%M%S')
    temp = tempfile.TemporaryDirectory(dir=maindir)
    print("\n\n*** RECUPERO LOG OVERGATE ***")
    print("*** Premere Enter o Y per confermare, X per rifiutare, CTRL+C per uscire ***\n")

    try:
        ### CHIEDO SE SCARICARE IL FILE UPD DALLA /temp
        if userInput(param="\n[?] Vuoi scaricare il file UPD* dalla /temp? ") == True:
            print("\n[+] Checking for files..  ") 
            downloadUPDFile()

        ### RECUPERO INFO DEL PV (PV E NUMERO FILIALE)
        getpvinfo = getPvInfo()
        if getpvinfo == False:
            sys.exit()
        ip = getpvinfo[0]
        numerofiliale = getpvinfo[1]

        ### VERIFICO LA CONNESSIONE ALLA CARTELLA CONDIVISA
        if connectToSharedFolder(ip) == False:
            sys.exit()

        ### DATA INIZIO / DATA FINE
        print("\n[+] Data inizio: ") 
        start = validateDate()
        print("\n[+] Data fine: ") 
        end = validateDate()

        ### RECUPERO DEI FILE
        if userInput(param="\n[?] Vuoi recuperare la PPOS/run? ") == True:
            print("\n[+] Recupero PPOS/run... ") 
            recuperoPPOS(dir=r"\c-drive\PPOS\RUN")
        if userInput(param="\n[?] Vuoi recuperare i log di Overgate?  ") == True:
            print("\n[+] Recupero Overgate log... ") 
            recuperoFile(dir=r"\c-drive", name="Trace", ext="txt")         
        if userInput(param="\n[?] Vuoi recuperare i log della stampante?  ") == True:
            print("\n[+] Recupero FiscalPrinter log... ") 
            recuperoFile(dir=r"\c-drive\Log\DitronRT", name="RTF", ext="log")

        ### CONTROLLO SE LA CARTELLA TEMP E' VUOTA 
        if len(os.listdir(temp.name)) == 0:
            input("\n[X] La cartella di destinazione risulta vuota!\n\n[>>] Press any key to exit program: \n")
            sys.exit()
        
        else:
            nomefile = "fil" + numerofiliale + "_" + today
            ### CHIEDO SE ZIPPARE LA CARTELLA DI DESTINAZIONE, ALTRIMENTI RINOMINO LA CARTELLA TEMP
            if userInput(param="\n[?] Vuoi zippare la cartella di destinazione?  ") == True:
                print("\n[+] Zipping files... ")
                zip = shutil.make_archive(os.path.join(maindir, nomefile), 'zip', temp.name)
                print("[+] OK! Zip file is: " + zip)
                ### INVIO IL FILE ZIP IN "public/Retail/temp, SE FALLISCE RINOMINO LA CARTELLA TEMP
                if userInput(param="\n[?] Vuoi caricare il file zip in pos.ditronetwrok/public/Retail/temp ?  ") == True:
                    print("\n[+] Uploading file zip...") 
                    if trasferisciFTP(dir=zip, filename=nomefile) == True:
                        print("[+] File caricato con successo!\n")
                else:
                    renameTempDir(temp.name, nomefile, maindir)
            else:
                renameTempDir(temp.name, nomefile, maindir)
        ### FINE
        input("\n[+] Fine.\n[>>] Press any key to exit program: \n")
    except KeyboardInterrupt as kerr:
        print(kerr)
