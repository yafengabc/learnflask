import gevent.monkey
gevent.monkey.patch_all()
import hashlib
import redis
from bottle import run,route,get,post,request
import check
import os
import config

base=config.files_dir
baseb=base.encode()
db=redis.Redis()
@post('/check')
def CheckHash():
    return db.get(request.body.read())
    pass

@post('/push')
def PushFile():
    pass

@post('/checkpath')
def Checkpath():
    path=request.body.read()
    dir,file=os.path.split(path)
    if os.path.exists(baseb+dir):
        return "Path OK"
    else:
        os.makedirs(baseb+dir)
        return "file not exits maked it!"
    #return check.hashfile(request.body.read())
    pass

@post('/fileok')
def FileOK():
    file,hash=eval(request.body.read())
#    print(result)
    if check.hashfile(base+file)==hash:
        db.set(file,hash)
        return("File Hash Checked OK")
        pass
    else:
        os.remove(base+file)
        return "Hash Checked Not OK,The file deleted"
    pass



run(server="gevent",host="0.0.0.0")
    
