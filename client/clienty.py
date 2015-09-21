import urllib.request
import urllib.parse
from ftplib import FTP
import hashlib
import os
import check
import config

host=config.server
file_sync=config.files_dir

def index_file(path):
    result={}
    for i in os.walk(path):
        for j in i[2]:
           result[os.path.join(i[0],j)]=check.hashfile(os.path.join(i[0],j))
    return result
def FileSync(path):
    filelist=index_file(path)
    for i in filelist:
        req=urllib.request.urlopen(host+'check',i.encode()).read()
        if req.decode()==filelist[i]:
            print('File "{}" already in server passed'.format(i))
        else:
            #print(i,filelist[i])
            print(Upload(i))
            print(CheckFile(i,filelist[i]))

def Upload(file):
    req=urllib.request.urlopen(host+'checkpath',file.encode()).read()
#    print(req)

    ftp=FTP()
    ftp.connect("127.0.0.1")
    ftp.login('root','88483273')
    ftp.storbinary('STOR '+base+file,open(file,'rb'))
    return 'The File:'+file+" Synced OK"
def CheckFile(file,hash):
    data=[file,hash]
    req=urllib.request.urlopen(host+'fileok',str(data).encode()).read()
#    print(req)
    return 'The File:'+file+" Checked OK"



FileSync(file_sync)
