import sys
import os
import os.path
import datetime
from datetime import datetime
from java.util import Date
from java.text import SimpleDateFormat

#dt = i.strftime('%d%m%Y')
#dt_time = i.strftime('%d%m%Y %H:%M:%S')
now = datetime.now()
#now = datetime.datetime.now()

connect("weblogic","passw0rd","t3://172.16.3.125:7001")
cd('domainRuntime:/ServerRuntimes/lms02');
date_MS_old = SimpleDateFormat('yyyy, MM, dd, HH, mm').format(java.util.Date(cmo.getActivationTime()))
date_now_old = now.strftime("%Y, %m, %d, %H, %M")

print date_MS_old
print date_now_old


#date_MS = datetime(2016, 12)  # ' + str(type(date_MS_old)) + ')'
#date_now = datetime(date_now_old)

#print date_MS
#print date_now
#difference = str(date_now) - str(date_now)
#print difference
