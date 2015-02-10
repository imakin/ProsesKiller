#!/usr/bin/env python
import os,sys
folder = "/media/kentir1/Development/Linux_Program/Fundkeep/"
try:
	argument = sys.argv[1]
except:
	argument = 0

def makinGetYear():
	return os.popen("date +'%Y'").read()[:-1]
def makinGetMonth():
	return os.popen("date +'%m'").read()[:-1]
def makinGetDay():
	return os.popen("date +'%d'").read()[:-1]

def makinGetPrevYear(daypassed):
	return os.popen("date --date='"+str(daypassed)+" day ago' +'%Y'").read()[:-1]
def makinGetPrevMonth(daypassed):
	return os.popen("date --date='"+str(daypassed)+" day ago' +'%m'").read()[:-1]
def makinGetPrevDay(daypassed):
	return os.popen("date --date='"+str(daypassed)+" day ago' +'%d'").read()[:-1]
	

os.system("mkdir "+folder+"data")
os.system("mkdir "+folder+"data/installment")



if argument=="edit":
	os.system("gedit "+folder+"data/installment/date")

data = ""
try:
	f = open(folder+"data/installment/date","r")
	data = f.read()
	f.close()
except:
	os.system("notify-send 'Fundkeep (c) 2013 Makin' 'You must entry installment date first'")
	os.system("gedit "+folder+"data/installment/date")
	f = open(folder+"data/installment/date","r")
	data = f.read()
	f.close()

f = open(folder+"data/"+makinGetYear()+"/"+makinGetMonth()+"/"+makinGetDay()+"/balance_after","r")
balance_after = str(int(f.read()))
f.close()
message = ""


i = 0
j = 0
j = data.find(" ")
l_day = (data[i:j])
data = data[j+1:]

j = data.find(" ")
l_month = (data[i:j])
data = data[j+1:]

j = data.find("\n")
l_year = (data[i:j])
data = data[j+1:]

print l_day
print l_month
print l_year

xxx = 0
while ((os.popen("date --date='"+str(xxx)+" day ago' +'%Y%m%d'").read()[:-1])!=((l_year)+(l_month)+(l_day))):
	xxx=xxx+1

if (xxx>1):
	message = message + "Your last installment was "+str(xxx)+" days ago.\n"
else:
	message = message + "Your last installment was "+str(xxx)+" day ago.\n"


j = data.find(" ")
n_day = (data[i:j])
data = data[j+1:]

j = data.find(" ")
n_month = (data[i:j])
data = data[j+1:]

j = data.find(" ")
n_year = (data[i:j])
data = data[j+1:]

print n_day
print n_month
print n_year

yyy = 0
while ((os.popen("date --date='"+str(yyy)+" day' +'%Y%m%d'").read()[:-1])!=((n_year)+(n_month)+(n_day))):
	yyy=yyy+1

if (yyy>1):
	message = message + "It must be spend wisely for the next "+str(yyy)+" days,\n"
else:
	message = message + "It must be spend wisely for the next "+str(yyy)+" day,\n"

#bikin tulisan format rupiah JATAH HARI INI DIKURANGI 4000 BRO
duit_c = int(balance_after)/(yyy+1)-4000
duit= ""
while (duit_c>999):
	duit = (str(duit_c)[-3:])+"."+duit
	duit_c = duit_c/1000
duit = ((str(duit_c)[-3:])+"."+duit)[:-1]
duit_c = duit_c/1000

message = message + "like around Rp "+duit+",00 a day from now on, which saves 20000 for 5 days fuel.\n"

balance_out = 0
try:
	f = open(folder+"data/"+makinGetYear()+"/"+makinGetMonth()+"/"+makinGetDay()+"/balance_out","r")
	data = f.read()
	f.close()
	cursor = data.find(" ")
	#~ if (data[:cursor]=="clr"):
		#~ balance_before = 0
	#~ else:
		#~ balance_out = balance_out + int(data[:cursor])
	balance_out = balance_out + int(data[:cursor])
	cursor = cursor + 1
	cursor = cursor + data[cursor:].find("\n")
	
	while (cursor!=(-1)):
		cursor_2 = data[cursor:].find(" ")
		cursor_2 = cursor + cursor_2
		
		#~ if (data[cursor:cursor_2])[1:4]=="clr":
			#~ balance_before = 0
		#~ else:
			#~ balance_out = balance_out + int(data[cursor:cursor_2])
		balance_out = balance_out + int(data[cursor:cursor_2])
		cursor = cursor_2 + 1
		cursor = cursor + data[cursor:].find("\n")
except:
	balance_out = balance_out
duit_c = int(balance_out)
duit= ""
while (duit_c>999):
	duit = (str(duit_c)[-3:])+"."+duit
	duit_c = duit_c/1000
duit = ((str(duit_c)[-3:])+"."+duit)[:-1]
duit_c = duit_c/1000
message = message+ "Thus, you have spent Rp "+duit+",00 today."

os.system("notify-send 'Fundkeep (c) makin 2013' '"+message+"'")
