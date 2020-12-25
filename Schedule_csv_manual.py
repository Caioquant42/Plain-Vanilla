#!/usr/bin/env python
# coding: utf-8

# In[7]:


import schedule
import os
import datetime  
import time
#import pytz  #timezone Brazil/DeNoronha


# In[8]:


current_time = datetime.datetime.now()
weekno = datetime.datetime.today().weekday()
hora,minuto = current_time.hour, current_time.minute
print(f"A hora atual é {current_time}\n \n")
print("Coloque a hora inicial inferior ou igual da hora atual:\n")
ini_h = int(input())
print("Coloque a minuto inicial:\n")
ini_m = int(input())
print("Coloque a hora final:\n")
fim_h = int(input())
print("Coloque o minuto final:\n")
fim_m = int(input())
print(f"A hora atual é {current_time} o intervalo de requesição será entre {ini_h}:{ini_m}-->{fim_h}:{fim_m}")
def work():
    exec(open("Scrape_liquid_csv.py").read())
    
    


# In[9]:


if weekno < 5:
    print(f"Hoje tem pregão!\n \n o mercado vai abrir as {ini_h} e {ini_m} minutos")
    go = True
    while go:
        current_time = datetime.datetime.now()
        hora,minuto = current_time.hour, current_time.minute
        if (hora>=ini_h) and (minuto>=ini_m):
            print("mercado abriu!")
            schedule.every(42).seconds.do(work) #scrape_liquid demora 36 segundo para rodar
            while go:
                schedule.run_pending()
                time.sleep(1)
                current_time = datetime.datetime.now()
                hora,minuto = current_time.hour, current_time.minute
                if (hora>=fim_h) and (minuto>=fim_m):
                    go = False
                    print("fim de pregão")          
else:
    go = False
    print("Final de Semana! não tem pregão")   
    


# In[ ]:




