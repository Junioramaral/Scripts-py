import sys
import os
from java.lang import System
from java.util import Date
from java.text import SimpleDateFormat
t = Date()  # Current date will be returned to t
searchday=SimpleDateFormat("dd").format(t) # extracting only day from the today date e.g:  Jul 3 2009 returns 3 here
## Teste
#
# Script Pyton para analisar data do ultimo Restart no Weblogic
# Author: Junior Amaral - Sep/2014
# Consultoria: ilegra
# 
# Version 1.0 (08/09/2014)

import getopt

ucf='/tmp/wls.config'
ukf='/tmp/wls.key'

#========================
#Connect To Domain
#========================

def connectToDomain():
	connect('weblogic', 'passw0rd', url='t3://192.xxx.xxx.xxx:7001')
#	try:
#		if username != "":
#			#connect(username, password, adminUrl)
#			connect('weblogic', 'xxxxxx', url='t3://192.168.0.130:7001')
#			print 'Successfully connected to the domain\n'
#		else:
#			connect(userConfigFile=ucf, userKeyFile=ukf, url='t3://192.168.0.130:7001')
#			print 'Successfully connected to the domain\n'
#
#		except:
#			print 'The domain is unreacheable. Please try again\n'
#			exit()

#========================
#Guet Startup date in Servers Domain
#========================
def _getDateServer(ServerName):
	try:
		cd('domainRuntime:/ServerRuntimes/'+ServerName);
		ActivationTime1 = java.util.Date(cmo.getActivationTime())
		print 'Applicaiton = ' + cmo.getName() +'\t\t####  Startup Date: '+str(ActivationTime1)
#		sys.stdout.write("\n")
	except:
		print 'Error in getting current status of ' +ServerName+ '\n';
		print 'Please check logged in user has full access to complete the stop operation on ' +ServerName+ '\n';
		exit()

#========================
#List Servers Domain
#========================
def listMain():
	try:
		cd('/Servers')
		allServers=ls('/Servers', returnMap='true')
		print 'Entrar no For';
		for p_server in allServers:
			if p_server == 'AdminServer':
				continue
			else:
				_getDateServer(p_server);

	except Exception, e:
		sys.stdout.write("\n")
		print "Error Occured"

#========================
#Execute Block
#========================

connectToDomain();
listMain();
sys.stdout.write("\n")
disconnect();
exit();
