from _weakref import proxy
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from pip._vendor.progress import counter
from common.exts import db
from common.searchData import CJsonEncoder,srch_hash_data,r,database,cursor
from model.models import upload_img, imgs, information,equipment,wx_user
import tqdm
import threading
import time
import json
import os

SEPARATOR="<SEPARATOR>"#分隔符
#RecThread为线程类主要用于控制线程的创建和限制创建线程的上限，设置最大并发线程数为100，超过100后的线程就会处于等待状态，直到线程列表移除一个线程才可以就行

# 创建线程类
class RecThread(threading.Thread):
    tlist = []  # 用来存储队列的线程
    maxthreads = 100  # 最大并发线程数
    event = threading.Event()  # 用事件来让超过最大线程设置的并发程序等待
    lock = threading.Lock()  # 线程锁

    def __init__(self, target):
        threading.Thread.__init__(self)
        self.target = target  # run方法中执行的操作

    def run(self):
        try:
            self.target()
        except:
            print("接收完毕线程关闭")
        RecThread.lock.acquire()  # 获得线程锁
        RecThread.tlist.remove(self)  # 将线程从线程队列移除
        # 如果移除此完成的队列线程数刚好达到99，则说明有线程在等待执行，那么我们释放event，让等待事件执行
        if len(RecThread.tlist) == RecThread.maxthreads - 1:
            RecThread.event.set()  # 让等待的线程执行
            RecThread.event.clear()
        RecThread.lock.release()  # 释放线程锁

    def newthread(proxy, counter, target):  # 创建新线程
        RecThread.lock.acquire()  # 获得线程锁
        sc = RecThread(target)  # 创建线程类
        RecThread.tlist.append(sc)  # 将新建的线程加入线程队列
        RecThread.lock.release()  # 释放线程锁
        sc.start()  # 开启线程

    # 将新线程方法定义为静态变量，供调用
    newthread = staticmethod(newthread)


# 数据接收类
class autoReciveData:
    def __init__(self, ws):
        self.ws = ws

    def runThread(self):
        RecThread.lock.acquire()
        if len(RecThread.tlist) >= RecThread.maxthreads:
            # 如果目前线程队列超过了设定的上线则等待。
            RecThread.lock.release()
            RecThread.event.wait()  # scanner.event.set()遇到set事件则等待结束
        else:
            RecThread.lock.release()
        RecThread.newthread(proxy, counter, target=self.ctreate_ThreadPool())

        for t in RecThread.tlist:
            t.join()  # j 待线程的执行完成才继续

    def ctreate_ThreadPool(self):
        recived = self.ws.receive()
        if not recived is None:
            rec = str(recived, encoding="utf8")
            equip_code, t, number,resume = rec.split(SEPARATOR)                           
            # 接收传过来的用户名，设备id，时间戳，，图片数量，主题，描述
            equip = equipment.query.filter(equipment.equip_code == equip_code).first()  # 获取刚刚上传图片数据的id
            equip_id = str(equip.id)
            sql = 'select user_id from upload_img where equip_id=%s and number<%s' %(equip_id,30)
            cursor.execute(sql)
            data = cursor.fetchall()
            print(data,type(data))
            user_id = data[0][0]
            user = wx_user.query.filter(wx_user.id == user_id).first()  # 获取刚刚上传图片数据的id
            username = user.name
            self.ws.send("核对成功") 
            ###############此处直接调用信息处理类来处理信息############################
            if resume == 'False':
                d=Data_deal(number,equip_id)
                d.update_info()   
                for j in r.scan_iter('imgs*'):
                    r.delete(j)
                for k in r.scan_iter('upload_img*'):
                    r.delete(k)  
                for i in r.scan_iter("eqimfo*"): 
                    r.delete(i)
            number = int(number)  # 将number转为int型
            threadPool = ThreadPoolExecutor(max_workers=number, thread_name_prefix="pro")  # 根据用户上传的文件
            # 一个用户来访问就会开一个线程，然后根据他传过来的图片数量，开启线程池读取文件
            for i in range(number):
                future = threadPool.submit(self.re(username, user_id, t))  # j将线程提交到线程池
            time.sleep(3)
            threadPool.shutdown()
            print('接收完!')
            #返回信息给客户端图片接收完毕
                
                    

    def re(self, username,user_id, t):
        count = 0
        flag = False  # 循环读取的标识
        t0 = time.time()
        basepath=os.path.split(os.path.dirname(__file__))[0]
        while 1:  # 循环接收文件
            length = 0  # 已接受文件长度
            if count == 0:  # count说明传过来的是一个文件的文件名文件大小等信息
                recived = self.ws.receive()  # 接收信息
                if recived == None:  # 当接收到的数据为空说明没有传输过的文件，退出循环读取文件
                    print("目前用户还没有发送信息请等候：")
                    break
                rec = str(recived, encoding="utf8",errors='ignore')
                self.ws.send("0")
                filename, file_size, file_format= rec.split(SEPARATOR)
                # 根据分隔符分割各传过来的信息，即获取文件名，文件大小，用户名，设备ID
                file_size, afile_size = file_size.split(",")
                print(f"文件名：{afile_size}<-------->文件大小：{file_size}")
                filename = filename.split("/")[-1]  # 获取带扩招名的文件名
                file_size = int(file_size)
                afile_size = int(afile_size)
                if file_format == ".txt":
                    dire = "data/" 
                    
                else:
                    dire = "images/"

                file_path = Path(os.path.join(basepath, "static/"+ dire + username))  # 根据用户名创建文件夹
                base_path = Path(os.path.join(basepath,"static/"+ dire + username + "/" + t))   # 根据每次上传文件的时间戳创建文件夹
                if file_path.exists():  # 判断以用户名命名的文件夹是否存在
                    if base_path.exists():  # 当以用户名命名的文件夹存在，则判断以当前获取的时间戳命名的文件夹是否存在
                        if os.path.exists(filename):  # 判断发送的文件是否已经存在
                            # self.send(f"文件{filename}已经存在！")   
                            break                                            
                        else:
                            file_name = "static/"+ dire + username + "/" + t + "/" + filename
                            filename = os.path.join(basepath, "static/"+ dire + username + "/" + t + "/" + filename)  #路径拼接
                            # 设置图片的真实存储路径
                    else:  # 如果以用户名命名的文件存在，但不存在以当前获取的时间戳命名的文件夹,
                         #则为创建文件夹，并为其创建一个获取的时间戳的文件夹，用于存放其发送到服务器的图片 
                        os.mkdir(base_path)
                        file_name = "static/"+ dire + username + "/" + t + "/" + filename
                        filename = os.path.join(basepath, "static/"+ dire + username + "/" + t + "/" + filename)  #路径拼接
                else:  # 如果以用户名命名的文件夹不存在，则说明压根没登录过则为其创建一个以用户命名的文件夹，
                    # 并将获取其传输过来的时间戳为其创建一个文件用于存放本次上传的图片                   
                    os.mkdir(file_path)
                    os.mkdir(base_path)
                    file_name = "static/"+ dire + username + "/" + t + "/" + filename                  
                    filename = os.path.join(basepath, "static/"+ dire + username + "/" + t + "/" + filename)  #路径拼接

            if Path(filename).exists():  # 判断发送的文件是否已经存在
                local_size = os.path.getsize(filename)
                if local_size != afile_size:
                    # self.send(f"文件{filename}已经存在！")
                    pro_1 = tqdm.tqdm(range(file_size),f"接收续传文件", unit="B", unit_divisor=1024)  # 设置进度调条
                    with open(filename, "ab") as f:  # 写文件                    
                        for _ in pro_1:  # 根据进度条读取数据，即每次读取1024B的数据
                            bytes_read = self.ws.receive()
                            if bytes_read == None:
                                flag = True
                                print("第二次死了")
                                break
                            f.write(bytes_read)                        
                            length += len(bytes_read)  # 已经读取的多少长度的文件
                            self.ws.send(f"{length}")
                            pro_1.update(len(bytes_read))  # 更新进度条
                            count += 1  # 当count不为零说明开始接收文件内容
                            print(f"第二次接收了{length}字节------------",f"大小为{file_size}字节")
                            if length == file_size:  # 文件接收完
                                print("第二次正常")
                                flag = False
                                break #退出for循环但没有退出with的循环读取
           
            else:            
                pro_2 = tqdm.tqdm(range(afile_size), f"接收第1次文件", unit="B", unit_divisor=1024)  # 设置进度调条               
                with open(filename, "wb") as f:  # 写文件
                    for _ in pro_2:  # 根据进度条读取数据，即每次读取1024B的数据
                        bytes_read = self.ws.receive()
                        if bytes_read == None:
                            flag = True                    
                            print("第一次死了")
                            break
                        f.write(bytes_read)                                              
                        length += len(bytes_read)  # 已经读取的多少长度的文件
                        self.ws.send(f"{length}")                     
                        pro_2.update(len(bytes_read))  # 更新进度条
                        count += 1  # 当count不为零说明开始接收文件内容
                      
                        print(f"第一次接收了{length}字节------{count}------",f"文件总大小为{afile_size}字节")
                        if length == afile_size:  # 文件还没接收完                            
                            print("第一次正常")
                            flag = False
                            break #退出for循环但没有退出with的循环读取 
                                                  
            
            
            local_size = os.path.getsize(filename)                     
            if (flag == False) and (local_size == file_size):  # 一个文件已经接受完毕，退出循环读取但并没有退出最外层循
                print("数据处理")
                if file_format == ".txt":
                    upoload = upload_img.query.filter(
                        upload_img.user_id == user_id).order_by(upload_img.date.desc()).first()  # 获取刚刚上传图片数据的id
                    image_id = upoload.id  # 获取当前上传用户的id
                    file_name = '\'%s\'' % file_name
                    sql='update imgs set data_path=%s where upload_id=%s' %(file_name,image_id)
                    cursor.execute(sql)
                    database.commit()
                else:
                    upoload = upload_img.query.filter(
                        upload_img.user_id == user_id).order_by(upload_img.date.desc()).first()  # 获取刚刚上传图片数据的id
                    image_id = upoload.id  # 获取当前上传用户的id
                    img = imgs(upload_id=image_id, file_path=file_name, data_path=0)
                    db.session.add(img)
                    db.session.commit()
                break#退出while循环
# 数据库信息处理类
class Data_deal():
    def __init__(self,number, equip_id):
        self.number=number
        self.equip_id=equip_id

    def update_info(self):
        sql = 'update upload_img set number="'+self.number+'" where equip_id="'+self.equip_id+'" and number=0'
        cursor.execute(sql)
        database.commit()
