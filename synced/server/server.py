#################################################################################################
#  服务提供程序         
#
#
#
#
################################################################################################
import gevent.monkey
gevent.monkey.patch_all()
import hashlib
import redis
from bottle import run,route,get,post,request
import check
import os
import config
import time

timefmt='%Y%m%d-%H%M%S'
base=config.file_dir
baseb=base.encode()
db=redis.Redis()

@get('/snapshot')
def Snapshot():
    timesec=time.strftime(timefmt,time.localtime())
    snapcmd='btrfs subvol snapshot {0} {1}'.format(config.file_dir,config.base_dir+timesec) 
    os.system(snapcmd)
    return "Created snapshot: "+timesec +"\n"


##从数据库查询checksum并返回
@post('/check')
def CheckHash():
    return db.lindex(request.body.read(),0)
    pass
##从数据库查询时间并返回
@post('/checkdate')
def CheckDate():
    return db.lindex(request.body.read(),1)

##本来想用于http传输来着，现在暂时用FTP了
@post('/push')
def PushFile():
    pass

##通过Client传过来的文件路径，建立本地目录
@post('/checkpath')
def Checkpath():
    path=request.body.read()        ##读取文件地址
    dir,file=os.path.split(path)    ##拆分地址为路径+文件
    if os.path.exists(baseb+dir):   ##如果目录存在就啥也不干
        return "Path OK"
    else:
        os.makedirs(baseb+dir)      ##如果目录不存在，就新建目录
        return "file not exits maked it!"
    pass

##传输完成后，客户端发来校验信息，
@post('/fileok')    
def FileOK():
    file,hash,date=eval(request.body.read())
    print('debug:'+file+hash+str(date))
    if check.hashfile(base+file)==hash:     ##如果发来的文件md5==本地算出的MD5
        if db.llen(file)>0:
            print('db.llen'+str(db.llen(file))+file)
            db.ltrim(file,0,0)
        db.lpush(file,date,hash)                   ##就存储到数据库
        return("File Hash Checked OK")
        pass
    else:
        os.remove(base+file)                ##如果不一致就删掉文件
        return "Hash Checked Not OK,The file deleted"
    pass



run(server="gevent",host="0.0.0.0")
    
