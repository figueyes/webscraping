
import pandas as pd
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

respuesta = pd.DataFrame(data=None, columns=['Rut_Agente', 'Dv_Agente', 'Nombres', 'Apellido Paterno', 'Apellido Materno', 'Estado_Agente', 'Isapre', 'Fecha_Scraping'])

#Inicia Driver
driver = webdriver.Chrome(executable_path=os.path.abspath("C:\WEBDRIVER\chromedriver"))

#Lee base de Agentes

df_lt = pd.read_csv("BBDD_Agentes.csv", encoding='UTF-8', sep=';', header=0)
print ("Carga Datos - OK")

print("-- Inicio del Proceso --")
#Inicia el Recorrido

for x in range(0, df_lt.shape[0]):

    rut_Agente = int(df_lt.iloc[x,0])
    dv_Agente = str(df_lt.iloc[x,1])

    #Ingresa URL
    driver.get("http://webserver.superdesalud.gob.cl/bases/AgentesVentas.nsf/WebConsultaCiudadano")

    #Busca Inputs para rellenar
    input_rut_Agente = driver.find_element_by_name("RutAgente")
    input_dv_Agente = driver.find_element_by_name("DvAgente")

    #Inicia acciones
    actions = ActionChains(driver)

    #Completa Rut
    input_rut_Agente.send_keys(rut_Agente)
    #Cambia a input dv
    actions.send_keys(Keys.TAB)
    #Completa dv
    actions.move_to_element(input_dv_Agente).send_keys(dv_Agente).perform()

    #Click en Buscar
    buscar = driver.find_element_by_xpath('//*[@id="main"]/div[2]/table/tbody/tr/td/fieldset/div[2]/input[1]')
    buscar.click()

    #Sleep
    #pausa = random.randint(1,2)
    #time.sleep(pausa)


    #Recupera Resultados
    try:
        nombres = driver.find_element_by_xpath('//*[@id="main"]/div[2]/table/tbody/tr/td/fieldset/div[2]/table/tbody/tr[2]/td[2]/div/table/tbody/tr[4]/td[2]').text
        apellido_Paterno = driver.find_element_by_xpath('//*[@id="main"]/div[2]/table/tbody/tr/td/fieldset/div[2]/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]').text
        apellido_Materno = driver.find_element_by_xpath('//*[@id="main"]/div[2]/table/tbody/tr/td/fieldset/div[2]/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td[2]').text
        estado_Agente = driver.find_element_by_xpath('//*[@id="main"]/div[2]/table/tbody/tr/td/fieldset/div[2]/table/tbody/tr[2]/td[2]/div/table/tbody/tr[1]/td[2]/b').text
        aseguradora_Agente = driver.find_element_by_xpath('//*[@id="main"]/div[2]/table/tbody/tr/td/fieldset/div[2]/table/tbody/tr[2]/td[2]/div/table/tbody/tr[5]/td[2]').text   
        
    except:
        nombres = 'Agente no registrado'
        apellido_Paterno = 'Agente no registrado'
        apellido_Materno = 'Agente no registrado'
        estado_Agente = 'Agente no registrado'
        aseguradora_Agente = 'Agente no registrado'

    #Llena Dataframe
    respuesta.loc[x] = [rut_Agente, dv_Agente, nombres, apellido_Paterno, apellido_Materno, estado_Agente, aseguradora_Agente, time.strftime("%d/%m/%y")]

    #Escribe csv
    respuesta.to_csv("DataSet_Scraping_Agentes.csv", sep=';', encoding='UTF-8', line_terminator='\n', index=False)
    print("Procesados {procesados} de {total}".format(procesados=x+1,total=df_lt.shape[0]))

driver.close()
print("-- Fin del Proceso --")