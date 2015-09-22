import urllib.request
import urllib.parse
from ftplib import FTP
import hashlib
import os
import check
import config

host=config.server
file_sync=config.files_dir
#base_dir=config.remote_base
base_dir='.'

def get_file_size(path):
    #return os.path.getsize(path)
    return os.path.getmtime(path)

def index_file(path):
    for i in os.walk(path):     ##遍历本地目录
        for j in i[2]: 
            file=os.path.join(i[0],j)
            try:                ##如果可读，返回当前文件路径+MD5值
                yield file,get_file_size(file)
            except:             ##不可读，返回err信息
                yield os.path.join(i[0],j),"error"

def FileSync(path): 
    for i,j in index_file(path):    ##获取一个文件信息
        if j=='error':              ##错误就忽略
            continue
        req=urllib.request.urlopen(host+'checkdate',i.encode()).read() ##从服务器获取本文件的日期
        print(req,j)
        if req.decode()==str(j):         ##如果md5与本地的相同，忽略，否则上传
            print('File "{}" already in server passed'.format(i))
        else:
            print(Upload(i))
            k=check.hashfile(i)
            print(CheckFile(i,k,j))

def Upload(file):
    req=urllib.request.urlopen(host+'checkpath',file.encode()).read()
    try:
        ftp.storbinary('STOR '+base_dir+file,open(file,'rb'))
        return 'The File:'+file+" Synced OK"
    except:
        return "Faillt"
def CheckFile(file,hash,date):
    data=[file,hash,date]
    print(data)
    req=urllib.request.urlopen(host+'fileok',str(data).encode()).read()
    return 'The File:'+file+" Checked OK"


ftp=FTP()
ftp.connect("127.0.0.1")
ftp.login('syncer','syncer')

FileSync(file_sync)
