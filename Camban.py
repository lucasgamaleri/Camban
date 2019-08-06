import pandas as pd
from pandas import *#read_excel
import xlrd

#Definiciones y funciones
def print_full(x):
        pd.set_option('display.max_rows', len(x))
        print(x)
        pd.reset_option('display.max_rows')

#IMPORTACION DE BASE DE DATOS
demoras = input('Archivo de datos de demoras >> ')
produccion = input('Archivo de datos de produccion >> ')

#date = "31-07-2019"
#demoras = read_excel(date +' - Demoras.xlsx')
#demoras.set_index('Bobina')
#produccion = read_excel(date +'.xlsx')
#produccion.set_index('Bobina')

demoras = read_excel(demoras)
demoras.set_index('Bobina')
produccion = read_excel(produccion)
produccion.set_index('Bobina')



# Lista de refilados
produccion = produccion.assign(REFILADO=lambda x: produccion['Material Refilado']!=0)


# Lista de cambios de ancho
cambiodeancho = [True]
for i in range(0,len(produccion)-1):
    if produccion.at[i+1,'Ancho'] == produccion.at[i,'Ancho']:
        cambiodeancho.append(False)
    else:
        cambiodeancho.append(True)


# Lista de Lotes
lotes = []
index = []
count = 1
fecha = []
refil = []
producto = []
dimension = []
for i in range(1, len(produccion)):        
        if produccion.at[i-1,'Ancho'] == produccion.at[i,'Ancho']:
                count = count+1                
        else:
                if list(produccion.index)[i] in list(demoras.index): # and demoras.at[list(produccion.index)[i],'Duracion']>=3: #demoras.Duracion[list(produccion.index)[i]]>1: #
                        lotes.append(count)
                        fecha.append(produccion.at[list(produccion.index)[i],'Fecha Produccion'])
                        refil.append(produccion.at[list(produccion.index)[i],'REFILADO'])
                        producto.append(produccion.at[list(produccion.index)[i],'Grupo Calidad'])
                        dimension.append(str(produccion.at[list(produccion.index)[i],'Espesor'])+'x'+str(produccion.at[list(produccion.index)[i],'Ancho']))
                        count = 1
                else:
                        count = count+1

demoras = {'Bobina': demoras.Bobina, 'Duracion de la demora': demoras.Duracion }
demoras = pd.DataFrame(data=demoras)
print(demoras)
print('\n \n')
result = {'Fecha Produccion': fecha, 'Dimension': dimension,'Cantidad de bobinas en el lote': lotes, 'Refilado': refil, 'Producto': producto}
result = pd.DataFrame(data=result)
result.to_html('prueba.html')
print(result)