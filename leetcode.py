# https://oj.leetcode.com/accounts/login/ method : post
# https://oj.leetcode.com/problems/
# <td><span class="ac"> </span></td>
# next <td> is the target.

import urllib2
import cookielib
import urllib


mydir  = r'C:/Users/user/Documents/GitHub/leetcode/'
myhost = r'https://oj.leetcode.com' 


	
cookie   = cookielib.CookieJar()
handler  = urllib2.HTTPCookieProcessor(cookie)
urlOpener = urllib2.build_opener(handler)
urlOpener.open('https://oj.leetcode.com/')

csrftoken = ""
for ck in cookie:
    csrftoken = ck.value


login = "shadowmydx"
mypwd = "dbtxhsjhy"


values = {'csrfmiddlewaretoken':csrftoken,'login':login,'password':mypwd,'remember':'on'}
values = urllib.urlencode(values)
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6)Gecko/20091201 Firefox/3.5.6', \
           'Origin':'https://oj.leetcode.com','Referer':'https://oj.leetcode.com/accounts/login/'}



request = urllib2.Request("https://oj.leetcode.com/accounts/login/",values,headers=headers)

url = urlOpener.open(request)

page = url.read()

# all done !

def saveCode(code,title):
	global mydir
	f = open(mydir + title + '.cpp','w')
	f.write(code)

def downloadCode(refer,codeadd,title):
	global headers
	global urlOpener
	global myhost
	headers['Referer'] = refer
	request = urllib2.Request(codeadd,headers=headers)
	url = urlOpener.open(request)
	all = url.read()
	tar = "storage.put('cpp',"
	index = all.find(tar,0)
	start = all.find('class Solution',index)
	finis = all.find("');",start)
	code  = all[start:finis]
	toCpp = {'\u000D':'\n','\u000A':'','\u003B':';','\u003C':'<','\u003E':'>','\u003D':'=',\
	'\u0026':'&','\u002D':'-','\u0022':'"','\u0009':'\t','\u0027':"'",'\u005C':'\\'}
	for key in toCpp.keys():
		code = code.replace(key,toCpp[key])
	saveCode(code,title)

def findCode(address,title):
	global headers
	global urlOpener
	global myhost
	headers['Referer'] = address
	address += 'submissions/'
	print 'now is dealing ' + address + ': ' + title 
	request = urllib2.Request(address,headers=headers)
	url = urlOpener.open(request)
	all = url.read()
	tar = 'class="text-danger status-accepted"'
	index = all.find(tar,0)
	start = all.find('href="',index)
	finis = all.find('">',start)
	downloadCode(address,myhost + all[start + 6:finis],title) 
	
def findAdd(page):
	index = 0
	while 1:
		index = page.find('class="ac"',index)
		if index != -1:
			index += 1
			start = page.find('<td><a href="',index)
			finis = page.find('">',start)
			tmpfin = page.find('<',finis)
			title = page[finis + 2:tmpfin]
			findCode(myhost + page[start + 13:finis],title)
		else:
			break
			
# work begin
findAdd(page)
