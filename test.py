import threading
import time
import cv2 as cv

class counting(threading.Thread):
    running = True
    count = 0
    def __init__(self, count=0):
        threading.Thread.__init__(self)
        self.count = count

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            threadLock.acquire()
            self.count += 1
            threadLock.release()
            print("Counting: Count = {}".format(self.count))
            time.sleep(1)
    
class process():
    def processed(count):
        return count*10
    def output(count, draw4):
        return "Count is {} and draw4 is {}".format(count, draw4)


class draw4(threading.Thread):
    running = True
    tencount = 0
    tencount4 = 0
    def __init__(self, tencount = 0):
        threading.Thread.__init__(self)
        self.tencount = tencount
    
    def update(self, tencount):
        threadLock.acquire()
        self.tencount = tencount
        threadLock.release()
        # print("Tencount is {}".format(self.tencount))
    
    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            tencount4 = self.tencount * 4
            threadLock.acquire()
            self.tencount4 = tencount4
            threadLock.release()
            print("Tencount4 is {}".format(self.tencount4))
            time.sleep(1)



threadLock = threading.Lock()
countthread = counting()
draw4thread = draw4()

countthread.start()
draw4thread.start()

try:
    while True:
        processednum = process.processed(countthread.count)
        draw4thread.update(processednum)
        output = process.output(countthread.count, draw4thread.tencount4)
        print(output)
        time.sleep(1)
except KeyboardInterrupt:
    countthread.stop()
    draw4thread.stop()