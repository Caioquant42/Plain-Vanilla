#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
import lxml.html as lh
import pandas as pd
import time
import os
import datetime


# In[6]:


count=0
current_time = datetime.datetime.now()
dia, mes, ano = current_time.day, current_time.month, current_time.year
h,m,s1 =  current_time.hour, current_time.minute , current_time.second
path = os.getcwd()
lista =['PETR','BOVA','VALE','VVAR','BBDC','COGN','BBAS','USIM','ITUB',
       'MGLU','B3SA','IRBR','GGBR','ABEV','ITSA','CIEL','CSNA','JBSS','BRML','SUZB']
excel = 'xlsx'

date = f"{dia}_{mes}_{ano}"
last_call = f"last"
new_path = f"{path}\{date}_xlsx"
if os.path.isdir(new_path) is False:
    new_folder = os.mkdir(f"{path}\{date}_xlsx")    
else:
    print("Pasta Já criada!")

print(f"Toda Base de dados será salvo na pasta:\n\n {date}")
print(f"As Opções {lista} de todos os vencimentos estão sendo\n coletados com 15 minutos de atraso.")


# In[7]:


for ativo in lista:


	cookies = {
	    'ASPSESSIONIDAQDCABSQ': 'NBNBJFFDKGLAKDBMCMNKKLAN',
	    '__utmc': '103385669',
	    '__utmz': '103385669.1607466575.1.1.utmcsr=tradergrafico.com.br^|utmccn=(referral)^|utmcmd=referral^|utmcct=/opcoes/',
	    '_fbp': 'fb.1.1607466771203.806434286',
	    'ASPSESSIONIDCSDBBBTR': 'OIAAHBCAHOCLGDLPFDGCDGHD',
	    '__utma': '103385669.450859380.1607466575.1607534770.1607556175.4',
	}

	headers = {
	    'Connection': 'keep-alive',
	    'Cache-Control': 'max-age=0',
	    'Upgrade-Insecure-Requests': '1',
	    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.400',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	    'Sec-Fetch-Site': 'none',
	    'Sec-Fetch-Mode': 'navigate',
	    'Sec-Fetch-User': '?1',
	    'Sec-Fetch-Dest': 'document',
	    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
	}


	response = requests.get(f'https://tradergrafi.co/opcoes/?opc={ativo}', headers=headers, cookies=cookies)


	#Store the contents of the website under doc
	doc = lh.fromstring(response.content)

	#Parse data that are stored between <tr>..</tr> of HTML
	tr_elements = doc.xpath('//tr')
	# Next, let’s parse the first row as our header.

	#Create empty list
	col=[]
	i=0
	#For each row, store each first element (header) and an empty list
	for t in tr_elements[0]:
	    i+=1
	    name=t.text_content()
	    #print ('%d %s' %(i,name))
	    col.append((name,[]))

	#Since out first row is the header, data is stored on the second row onwards
	for j in range(1,len(tr_elements)):
	    #T is our j'th row
	    T=tr_elements[j]
	    
	    #If row is not of size 10, the //tr data is not from our table 
	    if len(T)!=len(col):
	        break
	    
	    #i is the index of our column
	    i=0
	    
	    #Iterate through each element of the row
	    for t in T.iterchildren():
	        data=t.text_content() 
	        #Check if row is empty
	        if i>0:
	        #Convert any numerical value to float
	            try:
	                data=float(data)
	            except:
	                pass
	        #Append the data to the empty list of the i'th column
	        col[i][1].append(data)
	        #Increment i for the next column
	        i+=1
            
    #Criar Dataframe dos dados coletados: 
    
	Dict={title:column for (title,column) in col}
	df=pd.DataFrame(Dict)
    #df.columns = ['Ticker','Hora','Últ.Cotação','Nº Negócios','Descrição','Vencimento', 'Exercício']

	if excel == 'xlsx':
		nome = f"{ativo}_{date}"
		df.to_excel(rf"{new_path}\{nome}_{last_call}.xlsx", index=False, header=True)
		s2 = current_time.second        
		count+=1
 


# In[8]:


s3 = abs(s2-s1)
print(f"Finalizado, {count} vezes em {s3} Segundos")

