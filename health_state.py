
# Descrição:  Collect information about HealtState
# Author:  Junior Amaral Apr/2006

# Crontab
# Coleta de HealthState - Junior Amaral
# */3 * * * * /home/oracle/ilegra/scripts_py/health_state.sh 7005 7006 >> /home/oracle/ilegra/Lheathstate/health_state.out 2>&1


## Import the string library
import string
import sys
import time as pytime
import ConfigParser, os
from java.lang import System

# Date Format
timestampNOW = pytime.strftime("%d-%m-%Y %H:%M:%S", pytime.localtime())
timestampLOG = pytime.strftime("%d%m%Y", pytime.localtime())

var_dirname="/home/oracle/imon/tmp/"			#-- Substituir pelo /home/imon/tmp
var_dirnameL="/home/oracle/ilegra/Lheathstate/logs/"

## Credential
ucf='/home/oracle/ilegra/storeUser/userConfigUKF'
ukf='/home/oracle/ilegra/storeUser/passConfigPKF'

## Connect to adminserver of domain
for urls in sys.argv[1:]:
        connect(userConfigFile=ucf, userKeyFile=ukf, url='t3://localhost:' + urls )

	## Get health of servers
	serverRuntime()

	serverName = cmo.getName()
	serverhealth = str(cmo.getOverallHealthState())

	system_state = serverhealth.split(",")
	var_system_state = filter(lambda x:'State' in x,system_state)[0]
	var_system_state = var_system_state.split(":")[1]

	system_ReasonCode = serverhealth.split(",")
	var_ReasonCode = filter(lambda x:'ReasonCode' in x,system_ReasonCode)[0]
	var_ReasonCode = var_ReasonCode.split(":")[1]

	## Get Number of Stucks
	cd('serverRuntime:/ThreadPoolRuntime/ThreadPoolRuntime/')
	getStuckCount = cmo.getStuckThreadCount() 
	getThroughput = int(cmo.getThroughput())
	getHogging = cmo.getHoggingThreadCount()

	## Debug
	print "#------ DEBUG ------#"
	print "vlr Stuck count"
	print getStuckCount
	print "Vlr var_system_state"
	print var_system_state + "|" + serverName
	print "Vlr var_ReasonCode"
	print var_ReasonCode
	print "Vlr 2"
	print serverhealth
	print "#----------------------------------------------#"
	print " "
	print timestampNOW
	## Component:threadpool,State:HEALTH_WARN,MBean:ThreadPoolRuntime,ReasonCode:[ThreadPool has stuck threads]
	## HEALTH_OK|lms09


	if str(var_system_state) == "HEALTH_OK":

		print "...HEALTH_OK..."
		fo = open ( var_dirname + "RESULT.WEBLOGIC_HEALTHSTATE_" + serverName , "w+" )
		fo.write( "HEALTH_OK|" + serverName);
		fo.close()
		fo = open ( var_dirnameL + timestampLOG + "_" + serverName + "_" + "HEALTH_OK.log" , "a+" )
		fo.write( timestampNOW + " - " + "HEALTH_OK in " + serverName + " Th " + str(getThroughput) + " H "  + str(getHogging) + " S " + str(getStuckCount) + '\n' );
		fo.close()

	elif str(var_system_state) == "HEALTH_CRITICAL":

		if getThroughput <= 10 and getHogging >= 30 and getStuckCount >= 10:
			fo = open ( var_dirname + "RESULT.WEBLOGIC_HEALTHSTATE_" + serverName , "w+" )
			fo.write( "HEALTH_CRITICAL|" + serverName);
			fo.close()
			fo = open ( var_dirnameL + timestampLOG + "_" + serverName + "_" + "HEALTH_CRITICAL.log" , "a+" )
			fo.write( timestampNOW + " - " + "HEALTH_CRITICAL in " + serverName + " ReasonCode " + str(var_ReasonCode) + '\n' );
			fo.write( timestampNOW + " - " + "HEALTH_CRITICAL in " + serverName + " Throughput: " + str(getThroughput) + " HoggingThreadCount: " + str(getHogging) + " StuckThreadCount: " + str(getStuckCount) + '\n' );
			fo.close()
		else:
			fo = open ( var_dirnameL + timestampLOG + "_" + serverName + "_" + "HEALTH_CRITICAL.log" , "a+" )
			fo.write( timestampNOW + " - " + "LOG - HEALTH_CRITICAL in " + serverName + " ReasonCode " + str(var_ReasonCode) + '\n' );
			fo.write( timestampNOW + " - " + "LOG - HEALTH_CRITICAL in " + serverName + " Throughput: " + str(getThroughput) + " HoggingThreadCount: " + str(getHogging) + " StuckThreadCount: " + str(getStuckCount) + '\n' );
			fo.close()				

	elif str(var_system_state) == "HEALTH_FAILED":

		fo = open ( var_dirname + "RESULT.WEBLOGIC_HEALTHSTATE_" + serverName , "w+" )
		fo.write( "HEALTH_FAILED|" + serverName);
		fo.close()
		fo = open ( var_dirnameL + timestampLOG + "_" + serverName + "_" + "HEALTH_FAILED.log" , "a+" )
		fo.write( timestampNOW + " - " + "HEALTH_FAILED in " + serverName + " ReasonCode " + str(var_ReasonCode) + '\n' );
		fo.write( timestampNOW + " - " + "HEALTH_FAILED in " + serverName + " Throughput: " + str(getThroughput) + " HoggingThreadCount: " + str(getHogging) + " StuckThreadCount: " + str(getStuckCount) + '\n' );
		fo.close()

	elif str(var_system_state) == "HEALTH_OVERLOADED":

			fo = open ( var_dirname + "RESULT.WEBLOGIC_HEALTHSTATE_" + serverName , "w+" )
			fo.write( "HEALTH_OVERLOADED|" + serverName);
			fo.close()
			fo = open ( var_dirnameL + timestampLOG + "_" + serverName + "_" + "HEALTH_OVERLOADED.log" , "a+" )
			fo.write( timestampNOW + " - " + "LOG - HEALTH_OVERLOADED in " + serverName + " ReasonCode " + str(var_ReasonCode) + '\n' );
			fo.write( timestampNOW + " - " + "LOG - HEALTH_OVERLOADED in " + serverName + " Throughput: " + str(getThroughput) + " HoggingThreadCount: " + str(getHogging) + " StuckThreadCount: " + str(getStuckCount) + '\n' );
			fo.close()

	elif str(var_system_state) == "HEALTH_WARN":

		if getThroughput <= 10 and getHogging >= 30 and getStuckCount >= 10:
			fo = open ( var_dirname + "RESULT.WEBLOGIC_HEALTHSTATE_" + serverName , "w+" )
			fo.write( "HEALTH_WARN|" + serverName);
			fo.close()
			fo = open ( var_dirnameL + timestampLOG + "_" + serverName + "_" + "HEALTH_WARN.log" , "a+" )
			fo.write( timestampNOW + " - " + "QUARENTENA - HEALTH_WARN in " + serverName + " ReasonCode " + str(var_ReasonCode) + '\n' );
			fo.write( timestampNOW + " - " + "QUARENTENA - HEALTH_WARN in " + serverName + " Throughput: " + str(getThroughput) + " HoggingThreadCount: " + str(getHogging) + " StuckThreadCount: " + str(getStuckCount) + '\n' );
			fo.close()
		else:
			fo = open ( var_dirname + "RESULT.WEBLOGIC_HEALTHSTATE_" + serverName , "w+" )
			fo.write( "HEALTH_OK|" + serverName);
			fo.close()
			fo = open ( var_dirnameL + timestampLOG + "_" + serverName + "_" + "HEALTH_WARN.log" , "a+" )
			fo.write( timestampNOW + " - " + "LOG - HEALTH_WARN in " + serverName + " ReasonCode " + str(var_ReasonCode) + '\n' );
			fo.write( timestampNOW + " - " + "LOG - HEALTH_WARN in " + serverName + " Throughput: " + str(getThroughput) + " HoggingThreadCount: " + str(getHogging) + " StuckThreadCount: " + str(getStuckCount) + '\n' );
			fo.close()

	elif str(var_system_state) == "LOW_MEMORY_REASON":

		if getThroughput <= 10 and getHogging >= 30 and getStuckCount >= 10:
			fo = open ( var_dirname + "RESULT.WEBLOGIC_HEALTHSTATE_" + serverName , "w+" )
			fo.write( "LOW_MEMORY_REASON|" + serverName);
			fo.close()
			fo = open ( var_dirnameL + timestampLOG + "_" + serverName + "_" + "LOW_MEMORY_REASON.log" , "a+" )
			fo.write( timestampNOW + " - " + "LOW_MEMORY_REASON in " + serverName + " ReasonCode " + str(var_ReasonCode) + '\n' );
			fo.write( timestampNOW + " - " + "LOW_MEMORY_REASON in " + serverName + " Throughput: " + str(getThroughput) + " HoggingThreadCount: " + str(getHogging) + " StuckThreadCount: " + str(getStuckCount) + '\n' );
			fo.close()
		else:
			fo = open ( var_dirnameL + timestampLOG + "_" + serverName + "_" + "LOW_MEMORY_REASON.log" , "a+" )
			fo.write( timestampNOW + " - " + "LOG - LOW_MEMORY_REASON in " + serverName + " ReasonCode " + str(var_ReasonCode) + '\n' );
			fo.write( timestampNOW + " - " + "LOG - LOW_MEMORY_REASON in " + serverName + " Throughput: " + str(getThroughput) + " HoggingThreadCount: " + str(getHogging) + " StuckThreadCount: " + str(getStuckCount) + '\n' );
			fo.close()	

