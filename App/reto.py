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



def ranking_usuario(lst, cantidad, parametro, orden):
    ranking=lt.newList("ARRAY_LIST",compareRecordIds)
    lt.insertionSort(lst, orden, parametro)
    for i in range(1,lt.size(lst)+1):
        if ranking['size'] < cantidad:
            pelicula = lt.getElement(lst, i)
            lt.addLast(ranking, pelicula)             
    return ranking

def compañias(lst):
    l_peliculas = lt.newList("ARRAY_LIST", compareRecordIds)
    for n in range(1,lt.size(lst)+1):
        f = lt.getElement(lst, n)
        lt.addLast(l_peliculas, f["production_companies"])
    return l_peliculas["elements"]

def idioma (lst, idioma):
	peliculas = lt.newList("ARRAY_LIST", compareRecordIds)
	for i in range(1,lt.size(lst)+1):
		f = lt.getElement(lst, i)
		if idioma.lower() == f["original_language"].lower():
			lt.addLast(peliculas, f["title"])
	return peliculas

def conocerdirector(lst, lst2, director):
    l_peliculas = lt.newList("ARRAY_LIST", compareRecordIds)
    contador = 0
    valoracion = 0
    tupla = () 
    for n in range(1,lt.size(lst)+1):
        pelicula = lt.getElement(lst, n)
        n_director = lt.getElement(lst2, n)
        if director.lower()==n_director["director_name"].lower():
            lt.addLast(l_peliculas, pelicula["title"])
            contador += 1
            valoracion += float(pelicula["vote_average"])
    promedio = valoracion/contador
    tupla = (l_peliculas["elements"],contador, promedio)
    return tupla



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



def genero_pelicula(lst, genero):
    l_peliculas = lt.newList("ARRAY_LIST", compareRecordIds)
    contador = 0
    valoracion = 0
    tupla = ()
    for n in range(1,lt.size(lst)+1):
        pelicula = lt.getElement(lst, n)
        if genero.lower()==pelicula["genres"].lower() or genero.lower() in pelicula["genres"].lower():
            lt.addLast(l_peliculas, pelicula["title"])
            contador += 1
            valoracion += float(pelicula["vote_average"])
    promedio = valoracion/contador
    tupla = (l_peliculas,contador, promedio)
    return tupla



def rankingGenero(lst, cantidad, genero, parametro, orden):
    tupla = ()
    contador = 0
    l_peliculas = lt.newList("ARRAY_LIST", compareRecordIds)
    lt.insertionSort(lst, orden, parametro)  
    for n in range(1,lt.size(lst)+1):
        if l_peliculas['size'] < cantidad:
            pelicula = lt.getElement(lst, n)
            if genero.lower()==pelicula["genres"].lower() or genero.lower() in pelicula["genres"].lower():
                lt.addLast(l_peliculas, pelicula) 
                if parametro == "vote_average":
                    contador += float(pelicula["vote_average"])
                elif parametro == "vote_count":
                    contador += int(pelicula["vote_count"])      
    promedio = contador/lt.size(l_peliculas)
    tupla = (l_peliculas['elements'], promedio)                
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
                cantidad = 0 
                while cantidad < 10:
                    cantidad = int(input("Ingrese la cantidad de peliculas mayor de diez: "))
                parametro = input("Ingrese el digito 0 si quiere buscar por voto promedio o 1 si quiere por cantidad de votos: ")
                orden = input("Ingrese 1 si quiere que sea en orden descendente o 0 si desea que sea en orden ascendente: ")
                if int(parametro) == 0:
                    parametro = "vote_average"
                elif int(parametro) == 1:
                    parametro = "vote_count"
                if int(orden) == 0:
                    orden = "less"
                elif int(orden) == 1:
                    orden = "greater"
                print(ranking_usuario(lstmovies, cantidad, parametro, orden))

            elif int(inputs[0])==3: #opcion 3
                nombre_director=input("Inserte el nombre del director a buscar: ")
                print(conocerdirector(lstmovies,lstmovies2,nombre_director))

            elif int(inputs[0])==4: #opcion 4
                nombre_actor=input("Inserte el nombre del actor a buscar: ")
                print(actor_info(nombre_actor,lstmovies,lstmovies2))
                
            elif int(inputs[0])==5: #opcion 5
                genero = input("Ingrese el género de las películas: ")
                datos = genero_pelicula(lstmovies, genero)
                print(datos)

            elif int(inputs[0])==6: #opcion 6
                cantidad = 0
                while cantidad < 10:
                    cantidad = int(input("Ingrese la cantidad (mayor a 10) de las películas que desea buscar: "))
                genero = input("Ingrese el género de las películas: ")
                parametro = input("Ingrese el digito 0 si quiere buscar por voto promedio o 1 si quiere por cantidad de votos: ")
                orden = input("Ingrese 1 si quiere que sea en orden descendente o 0 si desea que sea en orden ascendente: ")
                if int(parametro) == 0:
                    parametro = "vote_average"
                elif int(parametro) == 1:
                    parametro = "vote_count"
                if int(orden) == 0:
                    orden = "less"
                elif int(orden) == 1:
                    orden = "greater"
                print(rankingGenero(lstmovies, cantidad, genero, parametro, orden))
                
            elif int(inputs[0])==7: #opcion 7
                datos = compañias(lstmovies)
                print(datos)
                
            elif int(inputs[0])==8: #opcion 8
                ida = input("Ingrese el idioma de las películas: ")
                datos = idioma(lstmovies, ida)
                print(datos)

            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()