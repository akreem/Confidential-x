import time
from celery import Celery
from celery.utils.log import get_task_logger

import oracledb
import os
from datetime import datetime
from openpyxl import load_workbook
from urllib.parse import unquote

logger = get_task_logger(__name__)

app = Celery('tasks',
             broker='amqp://admin:mypass@rabbit:5672',
             backend='rpc://')

def create_oracle_connection():
    User = 'ISSAOUI'
    Password = 'pass*'
    Host = '192.168.0.x'
    Port = '1521'
    Service_name = 'Service_name'

    #Create a connection
    connection = oracledb.connect(user=User, password=Password, host=Host, port=Port, service_name=Service_name)
    return connection

def close_oracle_connection(connection):
    connection.close()


@app.task()
def longtime_add(x, y):
    logger.info('Got Request - Starting work ')
    time.sleep(4)
    logger.info('Work Finished ')
    return x + y

@app.task()
def cd_add(idtr,username,gharadh):
    logger.info('Got Request - Starting work ')
    time.sleep(1)
    usernameCD = username+"_cd"
    task_id= cd_add.request.id

    connection = create_oracle_connection()
    cur = connection.cursor()

    sqlquery = "alter session set nls_date_format = 'dd/mm/rrrr'"
    cur.execute(sqlquery)
    
    sqlquery2 = "BEGIN ISSAOUIPKG.TRANSFERT_ENQEXT_AUTO(:IDTRAVAIL, :GHARADH, :USERNAME); END;"
    logger.info(f'BEGIN ISSAOUIPKG.TRANSFERT_ENQEXT_AUTO({idtr}, {gharadh}, {usernameCD}); END;')
    cur.execute(sqlquery2, {'IDTRAVAIL': idtr, 'GHARADH': gharadh, 'USERNAME': usernameCD })

    datejob = datetime.now().strftime("%Y/%m/%d")

    sqlquery3 = "UPDATE CDJOB SET  TASK_STATUS='SUCCESS' where TASK_ID = :TASKID"
    cur.execute(sqlquery3,{'TASKID':task_id})
    connection.commit()
		
    close_oracle_connection(connection)
    logger.info('Work Finished ')

    return (f"Task with id_travail : {idtr} Succeeded")

def DeleteAllData():
	connection = create_oracle_connection()
	cur = connection.cursor()
	sqlquery = "DELETE FROM DBASE.PERSONNE_TEMP_ENQEXT"
	cur.execute(sqlquery)
	connection.commit()
	close_oracle_connection(connection)
