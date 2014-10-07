# -*- coding: UTF-8 -*-
import re
import urllib
import urllib2
import sys
import PyV8
import os
# 爬取爱漫画《sketdance》的全章页面
# 找到某一话
# 分析文件名，下载全话图片
	# 通过执行js代码，找到具体的文件名。
# 进入下一话
mydir = r'd:/sketdance/'
imghost = r'http://c4.mangafiles.com/Files/Images/'
tarhost = r'http://www.imanhua.com'
taraddr = r'http://www.imanhua.com/comic/862/'
headers = {'Referer':'http://www.imanhua.com/comic/862/list_82877.html',\
'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'}
tarRequest = urllib2.Request(taraddr,headers=headers)

def downloadParts(url,title):
	print 'now is downloading ' + title + ':'
	print url
	print title.decode('gb2312').encode('gbk')
	os.mkdir(mydir + title.decode('gb2312').encode('gbk'))
	firststart = url.find('comic/') + len('comic/')
	firstslash = url.find('/',firststart)
	parturl = url[firststart:firstslash + 1]
	sestart = url.find('_',30)
	sefinis = url.find('.',sestart)
	parturl = parturl + url[sestart + 1:sefinis] + '/'
	partsRequest = urllib2.Request(url,headers=headers)
	while 1:
		try:
			page = urllib2.urlopen(partsRequest)
		except:
			pass
		else:
			break
	page         = page.read()
	jscode       = re.compile(r'<script type="text/javascript">(.+?)</script>')
	jscode       = jscode.search(page)
	jscode       = jscode.group(1)
	if jscode.find('split') != -1:
		jscode = 'var hogo;' + jscode
		start  = jscode.find('return p')
		jscode = jscode[0:start] + 'hogo=p;' + jscode[start:]
		with PyV8.JSContext() as env1:
			env1.eval(jscode)
			vars = env1.locals
			jscode = vars.hogo
	fileinx = jscode.find('files":')
	fileinx = jscode[fileinx:]
	imgre   = re.compile(r'([^"]+(\.jpg|\.png))')
	imglst  = imgre.findall(fileinx)
	imglst  = [key[0] for key in imglst]
	for index,key in enumerate(imglst):
		if key.find('.jpg') != -1:
			flag = '.jpg'
		else:
			flag = '.png'
		print imghost + parturl + key
		if index == 0:
			headers['Referer']  = url
		else:
			headers['Referer']  = url + '?p=' + str(index)
		imgRequest = urllib2.Request(imghost + parturl + key,headers=headers)
		while 1:
			try:
				img = urllib2.urlopen(imgRequest)
			except:
				pass
			else:
				break
		f = open(mydir +  title + '/' + str(index) + flag,'wb')
		f.write(img.read())
		f.close()
		
def findTar(url):
	while 1:
		try:
			page  = urllib2.urlopen(tarRequest)
		except:
			pass
		else:
			break
	page  = page.read()
	first = u'SketDance漫画列表'
	first = first.encode('gb2312')
	index = page.find(first)
	start = index
	title = ""
	parts = u'第'
	parts = parts.encode('gb2312')
	while index != -1:
		index = page.find('title="' + parts,index)
		if index == -1:
			break
		finis = page.find('"',index + 7)
		title = page[index + 7:finis]
		start = page.rfind('href="',start,index)
		finis = page.find('"',start + 6)
		downloadParts(tarhost + page[start + 6:finis],title) 
		index += 1
		start = index
findTar(taraddr)