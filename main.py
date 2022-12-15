import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from flask import Flask,render_template,request, session, redirect,Response
import json 
from difflib import SequenceMatcher 
from selenium import webdriver 
import time 
from datetime import date 
import requests
import csv
import io
app= Flask(__name__,template_folder='template')

@app.get("/")
def hello():
    return render_template('simple.html')
@app.get('/getPlotCSV')
def getPlotCSV():
    def json_from_url(url):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        data_json = soup.find(id='initial-data').get('data-json')
        return json.loads(data_json)
    def Convert(a): 
        init = iter(a)  
        res_dct = dict(zip(init, init))  
        return res_dct  
    # Função que recebe url do anúncio
    # e mostra nome do vendedor, telefone,
    # descrição do produto e preço
    df=pd.DataFrame(columns=['Carro','Vendedor','Telefone','Telefone Descrição','Preço','Cidade','CEP','Descrição',])

    def mostra_dados_do_anuncio(url):
        a0=0
        k=''
        carro=''
        data = json_from_url(url)
        prop=data['ad']['properties']
        prop1=prop[1]['value']
        a=0
        b=""
        n_descri=""
        cep = data['ad']['location']['zipcode']
        cidade=data['ad']['location']['municipality']
        #print(cep[0:4])
        carro=prop1
        cidades=['Sobral','Massapê','Senador Sá','Pires Ferreira','Santana do Acaraú','Forquilha','Coreaú','Moraújo','Groaíras','Reriutaba', 'Varjota', 'Cariré', 'Pacujá', 'Graça', 'Frecheirinha', 'Mucambo', 'Meruoca', 'Alcântaras']
    #print(cep[0:4])
        carro=prop1
    #Municípios de Massapê, Senador Sá, Pires Ferreira, Santana do Acaraú, Forquilha, Coreaú, Moraújo, Groaíras, Reriutaba, Varjota, Cariré, Pacujá, Graça, Frecheirinha, Mucambo, Meruoca e Alcântaras, além de Sobra
        for x in cidades:
            if(cidade==x):
                    descricao = data['ad']['body']
                    phone =  data['ad']['phone']['phone']
                    user = data['ad']['user']['name']
                    preco = data['ad']['price']
                    while (a<len(descricao)-1):
                        b=descricao[a]+descricao[a+1]
                        if(b=="88" or b=="85"):
                            n_descri=descricao[a:a+15]+""+n_descri
                        a=a+1
                    df.loc[len(df)]=[carro,user,phone,n_descri,preco,cidade,cep,descricao]
    for x in range(0,1):
    # Pega a lista de produtos da área de eletrônicos
        url_eletronicos="https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-ce/regiao-de-juazeiro-do-norte-e-sobral?o="+str(x+1)
        data = json_from_url(url_eletronicos)

    # Entra em cada anúncio e mostra o telefone
    adList = data['listingProps']['adList']
    for anuncio in adList:
        subject = anuncio.get('subject')
        if subject: 
            #print('------------------------')
            #descricao = anuncio.get('subject')        
            url = anuncio.get('url')
            #print('Descricao do produto:',descricao)
            #print('URL do produto=',url)
            mostra_dados_do_anuncio(url)
    print(df)
    df.to_csv('b1.csv')
    fp=io.open("b1.csv", mode="r", encoding="utf-8")
    csv = fp.read()
    try:
        return Response(
            csv,
            mimetype="text/csv",
            headers={"Content-disposition":
                    "attachment; filename=myplot.csv"})
    except:
        return 'Erro'
    

    
    #return render_template('simple.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
if __name__ =='__main__':
    app.run(debug=True)