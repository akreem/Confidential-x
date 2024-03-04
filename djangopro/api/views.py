from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json
import oracledb

def create_oracle_connection():
    User = 'AISSAOUI'
    Password = 'AISSAOUI2020*'
    Host = '192.168.0.204'
    Port = '1521'
    Service_name = 'mydbase'

    #Create a connection
    connection = oracledb.connect(user=User, password=Password, host=Host, port=Port, service_name=Service_name)
    return connection

def close_oracle_connection(connection):
    connection.close()

def personnes(request, param):
    connection = create_oracle_connection()
    cur = connection.cursor()
    sql="SELECT * FROM DBASE.PERSONNE WHERE CIN=:CIN"
    cur.execute(sql,{'CIN':param})
    details = cur.fetchall()
    pers_details = []
    for pers in details:
        pers_details.append({
            'prenom': pers[1],
            'prenpere': pers[2],
            'prengpere': pers[3],
            'nom': pers[4],
            'sex': pers[5],
            'nomprenmere': pers[6],
            'datnais': pers[7].date().strftime("%d/%m/%Y") if pers[7] != None else '',
            'lieunais': pers[8],
            'datecin': pers[12].date().strftime("%d/%m/%Y") if pers[12] != None else '',
            'sitfam': pers[14],
            'residence': pers[15],
            'nationalite': pers[17],
            'profession': pers[18],

        })
    close_oracle_connection(connection)
    json_data= json.dumps(pers_details,ensure_ascii = False, default=str, indent=4).encode('utf-8')    

    return HttpResponse(json_data, content_type='application/json;charset=utf-8')
def personnesAPI(response):
    return HttpResponse("Welcome to API Personnes/cin")

def enqext(request, cin):
    connection = create_oracle_connection()
    cur = connection.cursor()
    sql = "SELECT * FROM DBASE.ENQUETE_EXT WHERE PERSONNE_CIN=:CIN"
    cur.execute(sql,{'CIN':cin})
    enqdetails = cur.fetchall()
    enq_details = []
    for enq in enqdetails:
        enq_details.append({
            'ID_DEM': enq[0],
            'REF_DEM': enq[1],
            'DATEREF': enq[2].date().strftime("%d/%m/%Y") if enq[2] != None else '',
            'ORIGINDEM': enq[3],
            'OBSERV': enq[4],
            'CODETYPENQ1': enq[5],
            'TYPENQ1': enq[6],
            'TADHMIN': enq[7],
            'SOCIETE': enq[8],
            'PERSONNE_CIN': enq[9],
            'ID_TRAVAIL': enq[10],
            'COD_SOCIETE': enq[11],
            'TYPE_ENQ_EXT_ID_TYPE': enq[12],
            'ENQ_EXT_CODTYP1': enq[13],
            'ID_UNITE': enq[14],
            'REFDEMENQ': enq[15],
            'DATREF': enq[16].date().strftime("%d/%m/%Y") if enq[16] != None else '',
            'RESENQ1': enq[17],
            'REFRES1': enq[18],
            'DATEREFRES1': enq[19].date().strftime("%d/%m/%Y") if enq[19] != None else '',
            'RESENQ2': enq[20],
            'REFRES2': enq[21],
            'DATEREFRES2': enq[22].date().strftime("%d/%m/%Y") if enq[22] != None else '',
            'RESENQINT': enq[23],
            'REFFICHENQ': enq[24],
            'DATEREFFICHENQ': enq[25].date().strftime("%d/%m/%Y") if enq[25] != None else '',
            'RESFINAL': enq[26],
            'AUTINST': enq[27],
            'REFRESFINAL': enq[28],
            'DATEREFRESFIN': enq[29].date().strftime("%d/%m/%Y") if enq[29] != None else '',
            'DUREE_SUIVI': enq[30],
            'CODE_DEM': enq[31],
            'ETAT_DEM': enq[32],
            'IDSOCIETE': enq[33],
            'ROLEINSOCIETE': enq[34],
            'USER_UPDATE': enq[35],
            'DATE_UPDATE': enq[36].date().strftime("%d/%m/%Y") if enq[36] != None else ''
        })
    close_oracle_connection(connection)
    json_data = json.dumps(enq_details, ensure_ascii = False, default=str, indent=4).encode('utf-8')
    return HttpResponse(json_data, content_type='application/json;charset=utf-8')    
