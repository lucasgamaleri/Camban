import pandas as pd
from pandas import *
import xlrd

#Definiciones y funciones
def print_full(x):
        pd.set_option('display.max_rows', len(x))
        print(x)
        pd.reset_option('display.max_rows')
count = 1
lotes = []
index = []
fecha = []
refil = []
producto = []
dimension = []
Condicion = True
status = False




def Buscar_NombreArchivo(): #IMPORTACION DE BASE DE DATOS
        cline = input('¿Ha cambiado el nombre de archivo agregando la fecha de produccion y demora? [y/n]')
        if cline == 'y':
                Condicion = True
        elif cline == 'n':
                Condicion = False
        else:
                raise ValueError('No ha introducido una opción correcta')
                status = False
        if Condicion:
                produccion = 'SGL_Produccion_DECAPADO_EDA_Decapado_EDA '+input('Fecha de datos de demoras (Ej: 09-Ago)>> ')+'.xlsx'
                demoras = 'SGL_Demoras_Decapado_EDA '+input('Fecha de datos de produccion >> ')+'.xlsx'
        else:
                produccion = 'SGL_Produccion_DECAPADO_EDA_Decapado_EDA.xlsx'
                demoras = 'SGL_Demoras_Decapado_EDA.xlsx'
        try:
                demoras = read_excel(demoras)
                #demoras.set_index('Bobina')
                produccion = read_excel(produccion)
                status = True
                return status, demoras, produccion
        except:
                status = False
                return status
        
while status != True:
        Buscar_NombreArchivo()



#HAY QUE HACER ALGO POR EL ESTILO, CREAR NUEVO DATAFRAME PARA PRODUCCION
#Y DEMORAS CON LA INFORMACION IMPORTADA PARA QUE SEA MAS FACIL DE ANALIZAR POR LOS ALGORITMOS
#demoras = {'Bobina': demoras.Bobina, 'Duracion de la demora': demoras.Duracion }
#demoras = pd.DataFrame(data=demoras)


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
print('Analizar las siguientes bobinas en el Gantt')
for i in range(1, len(produccion)):
    if cambiodeancho[i] == True:
        cambiodeancho[i] = 'SI'
        fechaproduccion = produccion.at[i,'Fecha Produccion']
        print('Fecha:', fechaproduccion ,' --- Bobina:', produccion.Bobina[i], ' --- Cambio de ancho:', cambiodeancho[i])
        

bobinademora=list(demoras.Bobina)
for i in range(1, len(produccion)):        
        if produccion.Ancho[i-1] == produccion.Ancho[i]:
                count = count+1                
        else:
                if produccion.Bobina[i] in bobinademora and count<10 and cambiodeancho[i]=='SI' and produccion.REFILADO[i]==True:
                        lotes.append(count)
                        fecha.append(produccion.at[i,'Fecha Produccion'])
                        refil.append(produccion.at[i,'REFILADO'])
                        producto.append(produccion.at[i,'Grupo Calidad'])
                        dimension.append(str(produccion.at[i,'Espesor'])+'x'+str(produccion.at[i,'Ancho']))
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
exit = input('Presione Enter para cerrar el programa...')
