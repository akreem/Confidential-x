from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from .forms import FindcustomlistmarForm
import oracledb
import os

# Create your views here.
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
def index(request):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = f"Hello, Akrem! The current date and time is {current_time}"
    return render(request, "indexm.html")

@login_required(login_url='/s4/login')
def home(request):
    return render(request, "homem.html")

@login_required(login_url='/s4/login')
def getcustomlistmar(request):
    if request.method == 'POST':
        form = FindcustomlistmarForm(request.POST)
        if form.is_valid():
            connection = create_oracle_connection()
            cursor = connection.cursor()
            datemarfrom = form.cleaned_data["datemarfrom"]
            datemarto = form.cleaned_data["datemarto"]
            sqlquery = "alter session set nls_date_format = 'dd/mm/rrrr'"
            cursor.execute(sqlquery)

            sql = "SELECT militaire_mat, date_mariage,DBASE.Grade.LIB_GRAD,dbase.personne.PRENOM, dbase.personne.NOM,dbase.unite.LIB_UNITE\
            FROM DBASE.Grade,dbase.unite,DBASE.DEM_MARIAGE inner join DBASE.PERSONNE on DBASE.PERSONNE.CIN = dbase.dem_mariage.PERSONNE_CIN\
            inner join DBASE.militaire on dbase.militaire.MAT = dbase.dem_mariage.MILITAIRE_MAT WHERE dbase.militaire.CODE_ORGANE = dbase.unite.ID_UNITE\
            AND dbase.militaire.CODEGRADE = DBASE.Grade.CODE_GRADE AND res_final is null\
            AND DATE_MARIAGE between to_date(:Datefrom,'DD/MM/YYYY') AND to_date(:Dateto,'DD/MM/YYYY')\
            ORDER BY date_mariage asc"
            cursor.execute(sql,{'Datefrom':datemarfrom,'Dateto': datemarto})
            results = cursor.fetchall()
            index = 1
            mar_list = []
            for mar in results:
                mar_list.append({
                    'index': index,
                    'mat': mar[0],
                    'datemar': mar[1].strftime("%d/%m/%Y"),
                    'grade': mar[2],
                    'prenom': mar[3],
                    'nom': mar[4],
                    'unite': mar[5],
                })
                index +=1
            close_oracle_connection(connection)
            return render(request, "getcustomlistmar.html", {"mar_list": mar_list, "form":form})
    else:
        form = FindcustomlistmarForm()
        return render(request, "getcustomlistmar.html", {"form": form})