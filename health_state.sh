#!/bin/bash

SERVER=$1
PORT=$2
HOME_MS=/home/oracle/ilegra/scripts_py
JAVA_HOME=/u01/Middleware/jdk1.7.0_51
IMON_HOME=/home/oracle/imon
IMON_TMP=${IMON_HOME}/tmp/RESULT.WEBLOGIC_HEALTHSTATE_${SERVER}
FILEAGE=`${IMON_HOME}/tools/FileAge.pl ${IMON_TMP}`

RUN=$(cat $HOME_MS/health_state_${SERVER}_running.log)
        if [ "$RUN" -eq "1" ]
           then
             exit 0
           else
             echo "1" > $HOME_MS/health_state_${SERVER}_running.log
        fi


${JAVA_HOME}/bin/java -cp /u01/Middleware/Oracle_Home/wlserver/server/lib/weblogic.jar weblogic.WLST ${HOME_MS}/health_state.py ${PORT} 2>&1
echo ${FILEAGE}

echo "0" > $HOME_MS/health_state_${SERVER}_running.log
