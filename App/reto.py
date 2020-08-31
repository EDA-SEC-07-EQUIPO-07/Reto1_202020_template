"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista .
"""

import config as cf
import sys
import csv

from ADT import list as lt
from DataStructures import listiterator as it


from time import process_time 



def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Ranking de peliculas")
    print("3- Conocer un director")
    print("4- Conocer un actor")
    print("5- Entender un genero")
    print("6- Crear ranking")
    print("0- Salir")




def compareRecordIds (recordA, recordB):
    if int(recordA['id']) == int(recordB['id']):
        return 0
    elif int(recordA['id']) > int(recordB['id']):
        return 1
    return -1



def loadCSVFile (file, cmpfunction):
    lst=lt.newList("ARRAY_LIST", cmpfunction)
    dialect = csv.excel()
    dialect.delimiter=";"
    try:
        with open(  cf.data_dir + file, encoding="utf-8") as csvfile:
            row = csv.DictReader(csvfile, dialect=dialect)
            for elemento in row: 
                lt.addLast(lst,elemento)
    except:
        print("Hubo un error con la carga del archivo")
    return lst


def loadMovies ():
    lst = loadCSVFile("theMoviesdb/SmallMoviesDetailsCleaned.csv",compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst



def loadMovies2 ():
    lst = loadCSVFile("theMoviesdb/MoviesCastingRaw-small.csv",compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst



def actor_info (nombre_actor,lstmovies,lstmovies2):
    l_peliculas=lt.newList("ARRAY_LIST", compareRecordIds)
    contador_peliculas=0
    valoracion=0
    directores={}
    tupla=()
    lista_directores=[]
    for i in range (1,(lstmovies['size']+1)):
        nombre=lt.getElement(lstmovies2,i)
        pelicula=lt.getElement(lstmovies,i)
        if nombre_actor.lower()==nombre["actor1_name"].lower() or nombre_actor.lower()==nombre["actor2_name"].lower() or nombre_actor.lower()==nombre["actor3_name"].lower() or nombre_actor.lower()==nombre["actor4_name"].lower() or nombre_actor.lower()==nombre["actor5_name"].lower():
            lt.addLast(l_peliculas,pelicula["title"])
            contador_peliculas=contador_peliculas+1
            valoracion=valoracion+float(pelicula["vote_average"])
            if not((nombre["director_name"]) in directores):
                directores[nombre["director_name"]]=1
            elif nombre["director_name"] in directores:
                directores[nombre["director_name"]]+=1
    nom_dic=list(directores.keys())
    num_dic=list(directores.values())
    max_dic=max(num_dic)
    i=0
    while i<len(nom_dic):
        if max_dic==directores[nom_dic[i]]:
            lista_directores.append(nom_dic[i])
        i=i+1
    promedio=valoracion/contador_peliculas
    tupla=(l_peliculas['elements'],promedio,lista_directores,contador_peliculas)
    return tupla



def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """


    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:

            if int(inputs[0])==1: #opcion 1
                lstmovies = loadMovies()
                lstmovies2 = loadMovies2()

            elif int(inputs[0])==2: #opcion 2
                pass

            elif int(inputs[0])==3: #opcion 3
                pass

            elif int(inputs[0])==4: #opcion 4
                nombre_actor=input("Inserte el nombre del actor a buscar: ")
                print(actor_info(nombre_actor,lstmovies,lstmovies2))
                
            elif int(inputs[0])==5: #opcion 5
                pass

            elif int(inputs[0])==6: #opcion 6
                pass


            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()