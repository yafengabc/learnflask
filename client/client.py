import urllib.request
import urllib.parse
from ftplib import FTP
import hashlib
import os
import check
import config

host=config.server
file_sync=config.files_dir
base_dir=config.remote_base

def index_file(path):
    result={}
    for i in os.walk(path):
        for j in i[2]:
            try: 
                yield os.path.join(i[0],j),check.hashfile(os.path.join(i[0],j))
            except:
                yield os.path.join(i[0],j),"error"

def FileSync(path):
    for i,j in index_file(path):
        if j=='error':
            continue
        req=urllib.request.urlopen(host+'check',i.encode()).read()
        if req.decode()==j:
            print('File "{}" already in server passed'.format(i))
        else:
            print(Upload(i))
            print(CheckFile(i,j))

ftp=FTP()
ftp.connect("127.0.0.1")
ftp.login('root','88483273')
def Upload(file):
    req=urllib.request.urlopen(host+'checkpath',file.encode()).read()
#    print(req)
    try:
        ftp.storbinary('STOR '+base_dir+file,open(file,'rb'))
        return 'The File:'+file+" Synced OK"
    except:
        return "Faillt"
def CheckFile(file,hash):
    data=[file,hash]
    req=urllib.request.urlopen(host+'fileok',str(data).encode()).read()
#    print(req)
    return 'The File:'+file+" Checked OK"



FileSync(file_sync)
