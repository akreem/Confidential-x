from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from .forms import CreateNewSoc
from .forms import UpdateEnqextint
from .forms import AsyncenqextForm, FindCourForm, FindcivilForm
from django.core.cache import cache
import oracledb
import os
import base64
import json
import redis
from urllib.parse import quote
from openpyxl import Workbook

redis_client = redis.StrictRedis(host='redis', port=6379, db=1)


# con = oracledb.connect(user="AISSAOUI", password="AISSAOUI2020*", host="192.168.0.204", port=1521, service_name="mydbase")
# Create your views here.
def main(request):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = f"Hello, Akrem! The current date and time is {current_time}"
    return HttpResponse(response)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('home')
        else:
            messages.success(request, ("إسم المستخدم أو كلمة السر غير صحيحة"))
            return HttpResponseRedirect('login')    
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect('home')
        else:
            return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    return HttpResponseRedirect('login')

@login_required(login_url='/s4/login')
def index(request):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = f"Hello, Akrem! The current date and time is {current_time}"
    return render(request, "index.html")

@login_required(login_url='/s4/login')
def home(request):
    return render(request, "home.html")

@login_required(login_url='/s4/login')
def home1(request):
    return render(request, "home1.html")

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

@login_required(login_url='/s4/login')
def get_soc(request):
    connection = create_oracle_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * from dbase.e_societe ORDER BY COD_SOCIETE DESC")
    socs = cursor.fetchall()
    socs_list = []
    index = 1
    for soc in socs:
        socs_list.append({
            'index': index,
            'code': soc[0],
            'name': soc[1],
            'address': soc[2],
            'tel': soc[3],
            'uid': soc[4],
            'namefr': soc[5],
        })
        index +=1    
    close_oracle_connection(connection)
    return render(request, "suivsociete.html", {"socs_list": socs_list})

@login_required(login_url='/s4/login')
def create_societe(response):
    if response.method == "POST":
        form = CreateNewSoc(response.POST)
        if form.is_valid():
            connection = create_oracle_connection()
            cursor = connection.cursor()
            cursor.execute("select MAX(COD_SOCIETE) from DBASE.E_SOCIETE")
            maxid = cursor.fetchone()[0]

            code = maxid +1
            n = form.cleaned_data["name"]
            u = form.cleaned_data["uid"]
            nfr = form.cleaned_data["namefr"]
            r = form.cleaned_data["res"]
            t = form.cleaned_data["tel"]

            sql_query = "INSERT INTO dbase.e_societe  (COD_SOCIETE, SOCIETE, ADRESSE_SOCIETE, NUM_TEL_SOCIETE, ID_UNIQUE, NOM_FR) values \
            (:COD_SOCIETE, :SOCIETE, :ADRESSE_SOCIETE , :NUM_TEL_SOCIETE, :ID_UNIQUE, :NOM_FR)"
            
            cursor.execute(sql_query, {'COD_SOCIETE': code,'SOCIETE': n, 'ADRESSE_SOCIETE': r, 'NUM_TEL_SOCIETE': t,'ID_UNIQUE': u, 'NOM_FR': nfr})
            connection.commit()
            close_oracle_connection(connection)
            return HttpResponseRedirect("societes")     
                   

    else:
        form = CreateNewSoc()

    return render(response, "createsociete.html", {"form": form})

@login_required(login_url='/s4/login')
def enqextint_update(response):
    if response.method == "POST":
        form = UpdateEnqextint(response.POST)
        if form.is_valid():
            connection = create_oracle_connection()
            cursor = connection.cursor()

            g = form.cleaned_data["gharadh"]
            tf = form.cleaned_data["TADHMINFROM"]
            tt = form.cleaned_data["TADHMINTO"]
            y = form.cleaned_data["YEAR"]
            rc = form.cleaned_data["REF_COUR"]
            dc = form.cleaned_data["DATE_COUR"]

            sql_query = "BEGIN DBASE.PKG_MYDBA.UPD_REF_ENQ_EXT(:GHARADH, :TADHMINFROM, :TADHMINTO, :YEAR, :REF_COUR, to_date( :DATE_COUR,'YYYY/MM/DD')); END;"
            cursor.execute(sql_query, {'GHARADH': g, 'TADHMINFROM': tf, 'TADHMINTO': tt, 'YEAR': y, 'REF_COUR': rc, 'DATE_COUR': dc})
            #connection.commit()
            close_oracle_connection(connection)
    else:
        form = UpdateEnqextint() 
       
    return render(response, "enqextint_update.html", {"form": form})    

@login_required(login_url='/s4/login')
def asyncenqext(response, param):
    if response.method == "POST":
        form = AsyncenqextForm(response.POST)
        if form.is_valid():
            connection = create_oracle_connection()
            cursor = connection.cursor()
            cursor.execute("select MAX(NORDRE) from DBASE.ENQUETE_EXT_ASYNC")
            maxid = cursor.fetchone()[0]
            if not maxid:
                maxid = 0

            nordre = maxid +1 
            cin = form.cleaned_data["cin"]
            nom = form.cleaned_data["nom"]
            prenom = form.cleaned_data["prenom"]
            prenpere = form.cleaned_data["prenpere"]
            prengpere = form.cleaned_data["prengpere"]
            nomprenmere = form.cleaned_data["nomprenmere"]
            sex = form.cleaned_data["sex"]
            lieunais = form.cleaned_data["lieunais"]
            datnais = form.cleaned_data["datnais"]
            datecin = form.cleaned_data["datecin"]
            sitfam = form.cleaned_data["sitfam"]
            residence = form.cleaned_data["residence"]
            nationalite = form.cleaned_data["nationalite"]
            profession = form.cleaned_data["profession"]
            idtravail = param
            idoperateur = response.user.username
            cod_societe = form.cleaned_data["cod_societe"]
            codtype = form.cleaned_data["codtype"]

            sql_query = "INSERT INTO DBASE.ENQUETE_EXT_ASYNC \
            VALUES (:CIN, :PRENOM, :PRENPERE, :PRENGPERE, :NOM, :SEX, :NOMPRENMERE, :DATNAIS, :LIEUNAIS , :DATECIN, :SITFAM, :RESIDENCE, :NATIONALITE, :PROFESSION, :NORDRE, :COD_SOCIETE, :ID_TRAVAIL, :ID_OPERATEUR, :CODTYPE) "
            cursor.execute(sql_query, {'CIN': cin,'PRENOM': prenom,'PRENPERE': prenpere,'PRENGPERE': prengpere,'NOM': nom,'SEX': sex,
            'NOMPRENMERE': nomprenmere,'DATNAIS': datnais,'LIEUNAIS': lieunais,'DATECIN': datecin,'SITFAM':sitfam,'RESIDENCE':residence,
            'NATIONALITE':nationalite,'PROFESSION':profession,'NORDRE':nordre,'COD_SOCIETE':cod_societe,'ID_TRAVAIL':idtravail,
            'ID_OPERATEUR':idoperateur,'CODTYPE':codtype})
            connection.commit()
            close_oracle_connection(connection)
            return HttpResponseRedirect("/s4/asyncenqextsave")
    else:
        form = AsyncenqextForm()
        connection = create_oracle_connection()
        cursor = connection.cursor()
        sqlq = "SELECT SE_TRAVAIL.REF_COUR,SE_TRAVAIL.DATE_COUR,SE_TRAVAIL.OBJ_COUR,SE_UNITE.ABR_AR_UNITE \
            from DBASE.SE_TRAVAIL INNER JOIN DBASE.SE_UNITE ON SE_TRAVAIL.ID_UNITE=DBASE.SE_UNITE.ID_UNITE \
            INNER JOIN DBASE.SE_NAVETTE_INT ON SE_NAVETTE_INT.ID_TRAVAIL  = SE_TRAVAIL.ID_TRAVAIL WHERE  \
            DBASE.SE_NAVETTE_INT.ID_SERVICE = 04 AND DBASE.SE_TRAVAIL.ID_TRAVAIL like :ID_T"
        cursor.execute(sqlq, {'ID_T':param})
        trav = cursor.fetchone()
        refcour = trav[0]
        datecour = trav[1].strftime("%d/%m/%Y")
        obj = trav[2]
        unite = trav[3]
    
        
    return render(response, "asyncenqext.html", {"form":form,"param":param,"refcour":refcour, "datecour":datecour, "obj":obj, "unite":unite})

@login_required(login_url='/s4/login')
def asyncenqextCommit(response):
    connection = create_oracle_connection()
    cursor = connection.cursor()
    cursor.execute("select (select count(*) from dbase.ENQUETE_EXT_ASYNC where ENQUETE_EXT_ASYNC.id_travail like se.id_travail) as countx, \
        se.id_travail,se.obj_cour,se.ref_cour,se.date_cour from dbase.se_travail se where id_travail in (select id_travail from dbase.ENQUETE_EXT_ASYNC)") 
    travs = cursor.fetchall()
    travs_list = []
    for trav in travs:
        travs_list.append({
            'countx': trav[0],
            'id': trav[1],
            'obj': trav[2],
            'refcour': trav[3],
            'datecour': trav[4].strftime("%d/%m/%Y"),
        })
    close_oracle_connection(connection)    
    return render(response, "asyncenqextsave.html", {"travs_list": travs_list})

@login_required(login_url='/s4/login')
def asyncenqextRunCommit(response, idtrav):
    connection = create_oracle_connection()
    cursor = connection.cursor()
    sqlquery = "CALL DBASE.TRANSFERT_ENQEXT_ASYNC(:IDTRAV)"
    cursor.execute(sqlquery, {'IDTRAV': idtrav})
    close_oracle_connection(connection)
    return HttpResponseRedirect("/s4/asyncenqextsave")
    
@login_required(login_url='/s4/login')
def findcour(request):
    #username = quote(base64.urlsafe_b64encode(user.encode('utf-8')))
    if request.method == 'POST':
        username = request.user.username
        session_id = request.session.session_key

        cache_key = f'username:{session_id}'
        redis_client.set(cache_key, username)
        redis_client.expire(cache_key, 36000)
        
        form = FindCourForm(request.POST)
        if form.is_valid():
            connection = create_oracle_connection()
            cursor = connection.cursor()
            refcour = form.cleaned_data["refcour"]
            datecour = form.cleaned_data["datecour"]
            sqlquery = "alter session set nls_date_format = 'dd/mm/rrrr'"
            cursor.execute(sqlquery)

            sql_query1 = "SELECT SE_TRAVAIL.ID_TRAVAIL,SE_TRAVAIL.REF_COUR,SE_TRAVAIL.DATE_COUR,SE_TRAVAIL.OBJ_COUR,SE_UNITE.ABR_AR_UNITE, \
            CDJOB.ID_TRAVAIL as hasjob \
            from DBASE.SE_TRAVAIL INNER JOIN DBASE.SE_UNITE ON SE_TRAVAIL.ID_UNITE=DBASE.SE_UNITE.ID_UNITE \
            INNER JOIN DBASE.SE_NAVETTE_INT ON SE_NAVETTE_INT.ID_TRAVAIL  = SE_TRAVAIL.ID_TRAVAIL \
            LEFT JOIN CDJOB on SE_TRAVAIL.ID_TRAVAIL = CDJOB.ID_TRAVAIL WHERE  \
            DBASE.SE_NAVETTE_INT.ID_SERVICE = 04 AND REF_COUR like :REF_COUR ORDER BY DATE_COUR DESC FETCH FIRST 10 ROWS ONLY"

            sql_query2 = "SELECT SE_TRAVAIL.ID_TRAVAIL,SE_TRAVAIL.REF_COUR,SE_TRAVAIL.DATE_COUR,SE_TRAVAIL.OBJ_COUR,SE_UNITE.ABR_AR_UNITE, \
            CDJOB.ID_TRAVAIL as hasjob \
            from DBASE.SE_TRAVAIL INNER JOIN DBASE.SE_UNITE ON SE_TRAVAIL.ID_UNITE=DBASE.SE_UNITE.ID_UNITE \
            INNER JOIN DBASE.SE_NAVETTE_INT ON SE_NAVETTE_INT.ID_TRAVAIL  = SE_TRAVAIL.ID_TRAVAIL \
            LEFT JOIN CDJOB on SE_TRAVAIL.ID_TRAVAIL = CDJOB.ID_TRAVAIL WHERE  \
            DBASE.SE_NAVETTE_INT.ID_SERVICE = 04 AND REF_COUR like :REF_COUR AND DATE_COUR like :DATE_COUR ORDER BY DATE_COUR DESC FETCH FIRST 10 ROWS ONLY"

            sql_query3 = "SELECT SE_TRAVAIL.ID_TRAVAIL,SE_TRAVAIL.REF_COUR,SE_TRAVAIL.DATE_COUR,SE_TRAVAIL.OBJ_COUR,SE_UNITE.ABR_AR_UNITE, \
            CDJOB.ID_TRAVAIL as hasjob \
            from DBASE.SE_TRAVAIL INNER JOIN DBASE.SE_UNITE ON SE_TRAVAIL.ID_UNITE=DBASE.SE_UNITE.ID_UNITE \
            INNER JOIN DBASE.SE_NAVETTE_INT ON SE_NAVETTE_INT.ID_TRAVAIL  = SE_TRAVAIL.ID_TRAVAIL \
            LEFT JOIN CDJOB on SE_TRAVAIL.ID_TRAVAIL = CDJOB.ID_TRAVAIL WHERE  \
            DBASE.SE_NAVETTE_INT.ID_SERVICE = 04 AND DATE_COUR like :DATE_COUR ORDER BY DATE_COUR,ID_TRAVAIL DESC FETCH FIRST 10 ROWS ONLY"

            if datecour:
                if refcour:
                    cursor.execute(sql_query2,{'REF_COUR': refcour, 'DATE_COUR': datecour})
                else:
                    cursor.execute(sql_query3,{'DATE_COUR': datecour})
            else:
                if refcour:
                    cursor.execute(sql_query1,{'REF_COUR': refcour})
                else:
                    return HttpResponseRedirect('/s4/findcour')
            if cursor:        
                results = cursor.fetchall()
                index = 1
                trav_list = []
                for trav in results:
                    trav_list.append({
                        'index': index,
                        'ID_TRAVAIL': trav[0],
                        'REF_COUR': trav[1],
                        'DATE_COUR': trav[2].strftime("%d/%m/%Y"),
                        'OBJ_COUR': trav[3],
                        'ABR_AR_UNITE': trav[4],
                        'hasjob': trav[5],
                    })
                    index += 1
                
                close_oracle_connection(connection)
                return render(request, "findcour.html", {"trav_list": trav_list, "form": form})
    else:
        form = FindCourForm()
        return render(request, "findcour.html", {"form": form})                 

@login_required(login_url='/s4/login')
def findcivil(request):
    if request.method == 'POST':
        form = FindcivilForm(request.POST)
        if form.is_valid():
            connection = create_oracle_connection()
            cursor = connection.cursor()
            cin = form.cleaned_data["cin"]
            prenom = form.cleaned_data["prenom"]
            nom = form.cleaned_data["nom"]
            prenpere = form.cleaned_data["prenpere"]
            prengpere = form.cleaned_data["prengpere"]
            nomprenmere = form.cleaned_data["nomprenmere"]
            if not cin and not prenom and not nom and not prenpere and not prengpere and not nomprenmere:
                return HttpResponseRedirect('home')
            cin_c=prenom_c=nom_c=prenpere_c=prengpere_c=nomprenmere_c=""
            if cin:
                cin_c = f"AND CIN LIKE '{cin}'"

            if prenom:
                prenom_c = f"AND PRENOM LIKE '%{prenom}%'"

            if nom:
                nom_c = f"AND NOM LIKE '%{nom}%'"

            if prenpere:
                prenpere_c = f"AND PRENPERE LIKE '%{prenpere}%'"

            if prengpere:
                prengpere_c = f"AND PRENGPERE LIKE '%{prengpere}%'"     

            if nomprenmere:
                nomprenmere_c = f"AND NOMPRENMERE LIKE '%{nomprenmere}%'"                 

            cursor.execute(f"SELECT * FROM DBASE.PERSONNE WHERE 1=1 {cin_c} {prenom_c} {nom_c} {prenpere_c} {prengpere_c} {nomprenmere_c} \
            FETCH FIRST 50 ROWS ONLY")
            if cursor:
                results = cursor.fetchall()
                index = 1
                pers_list = []
                for pers in results:
                    pers_list.append({
                        'index': index,
                        'cin': pers[0],
                        'prenom': pers[1],
                        'prenpere': pers[2],
                        'prengpere': pers[3],
                        'nom': pers[4],
                        'sex': pers[5],
                        'nomprenmere': pers[6],
                        'datnais': pers[7].strftime("%d/%m/%Y") if pers[7] else None,
                        'nationalite': pers[17],
                        'profession': pers[18],

                    })
                    index += 1
                close_oracle_connection(connection)
                return render(request, "findcivil.html", {"form":form, "pers_list":pers_list})    
    else:
        form = FindcivilForm()
        return render(request, "findcivil.html", {"form":form})    

@login_required(login_url='/s4/login')
def appliedprev(request, param):
    pers = get_applied_prev(param)
    max_object = max(pers, key=lambda x:x['index'])
    max_index = max_object['index']
    connection = create_oracle_connection()
    cursor = connection.cursor()
    sql2= "select * from dbase.se_travail where id_travail=:IDTRAV"
    cursor.execute(sql2, {'IDTRAV': param})
    travail = cursor.fetchall()
    travail_list = []   
    for t in travail:
        travail_list.append({
            'refcour': t[5],
            'datecour':t[8].strftime("%d/%m/%Y"),
            'objcour':t[9],
        })    
    close_oracle_connection(connection)
    return render(request, "appliedprev.html", {"pers": pers, "travail_list": travail_list, "idv": param, "max_index": max_index})


def get_applied_prev(param):
    cache_key = f'{param}_details'
    data = cache.get(cache_key)
    if not data:
        connection = create_oracle_connection()
        cursor = connection.cursor()
        sqlquery = "select  dbase.personne.cin, dbase.personne.prenom,dbase.personne.nom,dbase.enquete_ext.tadhmin\
        from DBASE.personne INNER JOIN dbase.enquete_ext on personne.cin = dbase.enquete_ext.personne_cin\
        where enquete_ext.id_travail=:IDTRAV and \
        cin IN (select  PERSONNE_CIN from DBASE.ENQUETE_EXT where PERSONNE_CIN in \
        (select PERSONNE_CIN from DBASE.ENQUETE_EXT where id_travail=:IDTRAV ) \
        group BY PERSONNE_CIN \
        having count(*)>1)\
        order by tadhmin"
        cursor.execute(sqlquery, {'IDTRAV': param})
        results = cursor.fetchall()
        data = []
        index = 1
        for p in results:
            data.append({
                'index': index,
                'cin': p[0],
                'prenom': p[1],
                'nom': p[2],
                'tadhmin': p[3],    
            })
            index +=1
        close_oracle_connection(connection)
        cache.set(cache_key, data, timeout=3600)
    return data     


@login_required(login_url='/s4/login')
def profile(request,cin):
    connection = create_oracle_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM DBASE.PERSONNE WHERE CIN = :CIN"
    cursor.execute(sql, {'CIN': cin})
    personne = cursor.fetchall()
    pers_l = []
    for pers in personne:
        pers_l.append({
            'cin' : pers[0],
            'prenom' : pers[1],
            'prenpere' : pers[2],
            'prengpere' : pers[3],
            'nom' : pers[4],
            'SEX': pers[5],
            'NOMPRENMERE': pers[6],
            'DATNAIS': pers[7].strftime("%d/%m/%Y") if pers[7] else None,
            'LIEUNAIS': pers[8],
            'DATECIN': pers[12].strftime("%d/%m/%Y") if pers[12] else None,
            'RESIDENCE': pers[15],
            'SITFAM': pers[14],
            'NATIONALITE': pers[17],
            'PROFESSION': pers[18],
        })
    close_oracle_connection(connection)
    return render(request, "profile.html" , {"pers": pers_l})
           

def export_to_excel(data,filename):
    wb = Workbook()
    ws = wb.active
    ws.sheet_view.rightToLeft = True

    ws.append(["ع/ر","رقم ب ت و","الإسم","اللقب"])
    for item in data:
        ws.append([item["index"], item["cin"], item["prenom"], item["nom"]])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachement; filename={filename}.xlsx'
    wb.save(response)
    return response

@login_required(login_url='/s4/login')
def exportapp4(request,param):
    data1 = get_applied_prev(param)
    file_name = param
    return export_to_excel(data1, file_name)

@login_required(login_url='/s4/login')
def cdjobs(request):
    connection = create_oracle_connection()
    cursor = connection.cursor()
    sql = "SELECT CDJOB.THE_USER,CDJOB.DATEJOB,CDJOB.ID_TRAVAIL,CDJOB.CODE,CDJOB.TASK_STATUS,\
    DBASE.SE_TRAVAIL.OBJ_COUR,DBASE.SE_TRAVAIL.DATE_COUR,DBASE.SE_TRAVAIL.REF_COUR FROM CDJOB INNER JOIN DBASE.SE_TRAVAIL \
    ON CDJOB.ID_TRAVAIL = DBASE.SE_TRAVAIL.ID_TRAVAIL ORDER BY CDJOB.ID DESC"
    cursor.execute(sql)

    jobs = cursor.fetchall()
    jobs_list = []
    index = 1
    for j in jobs:
        jobs_list.append({
            'index': index,
            'user': j[0],
            'datejob': j[1].strftime("%d/%m/%Y"),
            'idt': j[2],
            'gharadh': j[3],    
            'status': j[4],   
            'obj': j[5],
            'datecour': j[6].strftime("%d/%m/%Y"),
            'refcour': j[7],     
        })
        index +=1
    close_oracle_connection(connection)
    return render(request, "cdjobs.html", {"jobs": jobs_list})    

@login_required(login_url='/s4/login')
def cd_details(request, param):
    pers = get_applied_prev(param)
    connection = create_oracle_connection()
    cursor = connection.cursor()
    sql2= "SELECT dbase.personne.CIN,dbase.personne.PRENOM,dbase.personne.NOM,dbase.personne.PROFESSION,dbase.enquete_ext.TADHMIN \
    FROM dbase.enquete_ext INNER JOIN dbase.personne ON dbase.enquete_ext.PERSONNE_CIN  = dbase.personne.CIN \
    WHERE dbase.enquete_ext.ID_TRAVAIL =:IDTRAV ORDER BY TADHMIN"
    cursor.execute(sql2, {'IDTRAV': param})
    results = cursor.fetchall()
    pers_list = []
    index = 1
    for p in results:
        pers_list.append({
            'index': index,
            'cin': p[0],
            'prenom': p[1],
            'nom': p[2],
            'PROFESSION': p[3],
            'tadhmin': p[4],    
        })
        index +=1 

    max_object = max(pers_list, key=lambda x:x['index'])
    max_index = max_object['index']

    sql= "select * from dbase.se_travail where id_travail=:IDTRAV"
    cursor.execute(sql, {'IDTRAV': param})
    travail = cursor.fetchall()
    travail_list = []   
    for t in travail:
        travail_list.append({
            'refcour': t[5],
            'datecour':t[8].strftime("%d/%m/%Y"),
            'objcour':t[9],
        })        
    close_oracle_connection(connection)
    return render(request, "cdetails.html", {"pers": pers_list, "travail_list": travail_list, "max_index": max_index})