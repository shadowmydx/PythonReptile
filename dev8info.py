import urllib2
import re
from threading import Thread,Lock

listPage = []
listResu = []
listFilter = []
listFilter.append(re.compile(r'php'))
listFilter.append(re.compile(r'[Pp]ython'))
listFilter.append(re.compile(r'[jJ]ava[^Ss]'))

pageLock = Lock()
writLock = Lock()

openEnd  = False
analEnd  = False
 
target   = r'http://www.witmart.com/cn/web-design/jobs'
webhost  = r'http://www.witmart.com/cn/web-design/jobs'
numPages = 22

class ReadPageThread(Thread):
    def run(self):
        global listPage
        global target
        global numPages
        global pageLock
        global openEnd
        self.nextPage = 1
        while numPages != 0:
            f = self.openPage(target)
            pageLock.acquire()
            listPage.append(f)
            print target + ' is finished.' 
            pageLock.release()
            target = self.findNext(f)
            numPages -= 1
        openEnd = True
            

    def openPage(self,target):
        tmp = True
        while tmp:
            try:
                print 'open page..'
                f = urllib2.urlopen(target).read()
                print 'open successed!'
                break
            except:
                tmp = True
        return f
            

    def findNext(self,target):
        global webhost
        self.nextPage += 1
        return webhost + '?p=' + str(self.nextPage)
        
        
class AnalsPageThread(Thread):
    def run(self):
        global listPage
        global pageLock
        global openEnd
        global analEnd
        f = False
        while not openEnd or len(listPage) != 0:
            pageLock.acquire()
            if len(listPage) != 0:
                f = listPage.pop(0)
            else:
                f = False
            pageLock.release()
            if f != False:
                self.analsPage(f)
        analEnd = True

    def analsPage(self,target):
        global listResu
        global writLock
        global listFilter
        ul  = r'<ul class="joblist"'
        liItem  = re.compile(r'<li.*?</li>',re.DOTALL)
        ulStart = target.find(ul)
        
        target  = target[ulStart:]
        liList  = liItem.findall(target)

        for item in liList:
            # judge if has php
            for key in listFilter:
                if key.search(item):
                    writLock.acquire()
                    item = self.replaceHref(item)
                    listResu.append(item)
                    print 'analysis one item success!'
                    writLock.release()
                    break
    
    def replaceHref(self,item):
        return item.replace('/cn','http://www.witmart.com/cn')

class WritePageThread(Thread):
    def __init__(self,pathTo):
        Thread.__init__(self)
        self.pathTo = pathTo
    
    def run(self):
        global listResu
        global writLock
        global analEnd
        f = open(self.pathTo + '/' + 'res.html','wb')
        f.write(r'<html><body><ul>')
        while analEnd == False or len(listResu) != 0:
            writLock.acquire()
            if (len(listResu) != 0):
                liItem = listResu.pop(0)
                f.write(liItem)
                f.write('<br />')
                print 'write one item success!'
            writLock.release()
        f.write('</ul></body></html>')
        f.close()
        

a = ReadPageThread()
b = AnalsPageThread()
c = WritePageThread(r'/home/wmydx/info')

a.start()
b.start()
c.start()
