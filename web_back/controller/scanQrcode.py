from _weakref import proxy
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from geventwebsocket.websocket import WebSocket,WebSocketError
from pip._vendor.progress import counter
from common.exts import db
from common.searchData import CJsonEncoder,srch_hash_data,r,database,cursor
from model.models import upload_img, imgs, information, equipment
import tqdm
import threading
import time
#coding=utf-8
import json
import os
import time



SEPARATOR="<SEPARATOR>"#分隔符
# RecThread为线程类主要用于控制线程的创建和限制创建线程的上限，设置最大并发线程数为100，
# 超过100后的线程就会处于等待状态，直到线程列表移除一个线程才可以执行

#使用类定义thread，继承threading.Thread 
# 创建线程类
class RecThread(threading.Thread):
    tlist = []  # 用来存储队列的线程
    maxthreads = 20  # 最大并发线程数
    evnt = threading.Event()  # 用事件来让超过最大线程设置的并发程序等待
    lck = threading.Lock()  # 线程锁

    def __init__(self, target):
        threading.Thread.__init__(self)
        self.target = target  # run方法中执行的操作

    def run(self):
        try:
            self.target()
        except:
            print("启动脚本的线程关闭")
        RecThread.lck.acquire()  # 获得线程锁 #当需要独占RecThread资源时，必须先锁定，这个锁可以是任意的一个锁
        RecThread.tlist.remove(self)  # 将线程从线程队列移除
        # 如果移除此完成的队列线程数刚好达到99，则说明有线程在等待执行，那么我们释放event，让等待事件执行
        if len(RecThread.tlist) == RecThread.maxthreads - 1:
            RecThread.evnt.set()  # 让等待的线程执行
            RecThread.evnt.clear()
        RecThread.lck.release()  # 释放线程锁 #使用完RecThread资源必须要将这个锁打开，让其他线程使用 

    def newthread(proxy, counter, target):  # 创建新线程
        RecThread.lck.acquire()  # 获得线程锁
        sc = RecThread(target)  # 创建线程类
        RecThread.tlist.append(sc)  # 将新建的线程加入线程队列
        RecThread.lck.release()  # 释放线程锁
        sc.start()  # 开启线程

    # 将新线程方法定义为静态变量，供调用
    newthread = staticmethod(newthread)


# 启线程类
class startEquip:
    def __init__(self, ws, code):
        self.ws = ws
        self.code = code

    def runThread(self):
        RecThread.lck.acquire()
        if len(RecThread.tlist) >= RecThread.maxthreads:
            # 如果目前线程队列超过了设定的上线则等待。
            RecThread.lck.release()
            RecThread.evnt.wait()  # scanner.evnt.set()遇到set事件则等待结束
        else:
            RecThread.lck.release()
        RecThread.newthread(proxy, counter, target=self.ctreate_Thread())

        for t in RecThread.tlist:
            t.join()  # j 待SC线程的执行完成才继续

    def ctreate_Thread(self):
        equip_code = self.code
        d=Data_deal(equip_code)
        d.update_info()        
        while 1:
            self.ws.send('ping')  
            recived = self.ws.receive()
            if recived:
                pass
            else:
                time.sleep(5)
                if not recived: 
                    break
            time.sleep(5)

# 数据库信息处理类            
class Data_deal():
    def __init__(self,equip_code):
        self.equip_code=equip_code
       

    def update_info(self):
        equip = equipment.query.filter(equipment.equip_code == self.equip_code).first()
        #找到
        if not equip:
            equip_data = equipment(equip_name=0,equip_disc=0,if_work=0,equip_adr=0,
                equip_ip=0,equip_posi=0,equip_image=0,equip_code=self.equip_code)
            db.session.add(equip_data)
            db.session.commit()  
