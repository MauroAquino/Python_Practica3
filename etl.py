import csv
import time
from collections import Counter


class Etl:


    @classmethod
    def load_file(cls, file_name):

        """
        Esta funcion crea un set con las peliculas a fin de eliminar
        registros duplicados, luego carga el csv en una lista de diccionarios

        :param file_name: nombre de archivo a cargar
        :return: lista de diccionarios con la informacion de las peliculas
        """

        duplicate = set()
        movie_list = []
        with open(file_name, encoding="UTF-8") as csv_file:
            list_all = csv.DictReader(csv_file)
            for row in list_all:
                if row['movie_title'] in duplicate:
                    continue
                duplicate.add(row['movie_title'])
                movie_list.append(row)
        return movie_list


    #TODAS LAS FUNCIONES UTILIZAN LA LOGICA DE LEN(INDICE DE BUSQUEDA)>0 PARA ELIMINAR LOS REGISTROS DE BUSQUEDA VACIOS

    @classmethod
    def color_bn(cls,list):
        """
        Utiliza una funcion interna que accede tres veces
        para numerar los registros de cada tipo
        :param list: Lista de peliculas
        :return: Cantidad de elementos encontrados en base al indice de diccionario "Color"
        """

        def color_bn_traer(param):
            """
            Funcion interna que se ejecuta tres veces y busca los registros del indice "Color"
            :param param: Este parametro es Color, Blanco y Negro y Vacio
            :return: el len() de la lista con esos parametros
            """
            return len([row['movie_title'] for row in list if row['color'].strip() == param])

        return {'Color':color_bn_traer("Color"),'Blanco y Negro' : color_bn_traer("Black and White"), 'Vacio' : color_bn_traer("")}


    @classmethod
    def analysis_data_doub(cls,param_uno,param,list):
        """
        Comprehension de dos parametros que devuelve un ranking sorted por valor 2
        :param param_uno: indice de diccionario uno
        :param param: indice de diccionario dos (valor_numerico)
        :param list: lista de peliculas
        :return: devuelve una sublista formada por los registros de indice 1 y 2
        """

        return sorted([[row[param_uno].replace("\xa0", "").strip(), int(row[param])] for row in list if len(row[param])>0],key=(lambda x: x[1]))


    @classmethod
    def analysis_data_sing(cls, param_uno, list):
        """
        Comprehension de un parametros (utilizada para la funcion counter) devuelve
        la lista sorted por el primer valor
        :param param_uno: indice de diccionario uno
        :param list: lista de peliculas
        :return: devuelve una sublista formada por los registros de indice 1
        """

        return sorted(
            [[row[param_uno].replace("\xa0", "").strip()] for row in list],key=(lambda x: x[0]))


    @classmethod
    def counters_doub(cls, param_uno, param, param_dos, list):
        """
        Utiliza una comprehension y la funcion counter para crear un diccionario y
        consecuentemente una lista con los valores en base a los indices deseados
        de contabilizar para dos registros

        :param param_uno: indice uno de entrada a la funcion anaysis_data_doub
        :param param: indice dos de entrada a la funcion analysis_data_doub
        :param param_dos: indice de lista para criterio de comprehension
        :param list: lista de peliculas
        :return: Sub-Lista con criterio de cantidad de apariciones por registro
        """
        return sorted([[key, value] for key, value in Counter([a[param_dos] for a in Etl.analysis_data_doub(param_uno, param, list)]).items()], key=lambda x: x[1])


    @classmethod
    def counters_sing(cls, param_uno, param_dos, list):
        """
        Utiliza una comprehension y la funcion counter para crear un diccionario y
        consecuentemente una lista con los valores en base a los indices deseados
        de contabilizar para un registro

        :param param_uno: indice uno de entrada a la funcion anaysis_data_doub
        :param param_dos: indice de lista para criterio de comprehension
        :param list: lista de peliculas
        :return: Sub-Lista con criterio de cantidad de apariciones por registro
        """

        return sorted([[key, value] for key, value in Counter([a[param_dos] for a in Etl.analysis_data_sing(param_uno, list)]).items()],key=lambda x: x[1])

    @classmethod
    def menos_criticadas(cls,list):
        """
        Utiliza la funcion de analisis de dos parametros
        para traer cantidad de criticos por pelicula
        y conocer las peliculas con mayor cantidad de
        criticas
        :param list: lista de peliculas
        :return: top 10 de peliculas con mayor cantidad de criticas
        """
        return Etl.analysis_data_doub("movie_title","num_critic_for_reviews",list)[:10]

    @classmethod
    def mayor_duracion(cls, list):
        """
        Utiliza la funcion de analisis de dos parametros
        para traer duracion por pelicula
        y conocer las peliculas con mayor duracion
        :param list: lista de peliculas
        :return: top 20 de peliculas con mayor cantidad duracion
        """

        return Etl.analysis_data_doub("movie_title", "duration", list)[-20:]

    @classmethod
    def mayor_dinero(cls, list):
        """
        Utiliza la funcion de analisis para traer
        el gross por pelicula
        :param list: Lista de Peliculas
        :return: top 5 peliculas con mayor gross (utlimos 5 del sorted list)
        """
        return Etl.analysis_data_doub("movie_title", "gross", list)[-5:]

    @classmethod
    def menor_dinero(cls, list):
        """
        Utiliza la funcion de analisis para traer
        el gross por pelicula
        :param list: Lista de Peliculas
        :return: top 5 peliculas con menor gross (primeros 5 del array)
        """
        return Etl.analysis_data_doub("movie_title", "gross", list)[:5]

    @classmethod
    def mayor_presupuesto(cls, list):
        """
        Utiliza la funcion de analisis para traer
        el budget por pelicula
        :param list: Lista de Peliculas
        :return: top 3 peliculas con mayor gross (ultimos 3 del array)
        """
        return Etl.analysis_data_doub("movie_title", "budget", list)[-3:]

    @classmethod
    def menor_presupuesto(cls, list):
        """
        Utiliza la funcion de analisis para traer
        el budget por pelicula
        :param list: Lista de Peliculas
        :return: top 3 peliculas con mayor budget (primeros 3 del array)
        """

        return Etl.analysis_data_doub("movie_title", "budget", list)[:3]

    @classmethod
    def mayor_produccion(cls, list):
        """
        Utiliza la funcion de counter para traer
        la cantidad de peliculas por año
        :param list: Lista de Peliculas
        :return: año de mayor produccion (ultimo del array)
        """
        return Etl.counters_doub("movie_title","title_year",1,list)[-1:]

    @classmethod
    def menor_produccion(cls, list):
        """
        Utiliza la funcion de counter para traer
        la cantidad de peliculas por año
        :param list: Lista de Peliculas
        :return: año de menor produccion (primero del array)
        """
        return Etl.counters_doub("movie_title","title_year",1,list)[:1]

    @classmethod
    def pelicula_por_director(cls, list):
        """
        Utiliza la funcion de counter para traer
        la cantidad de peliculas por director
        :param list: Lista de Peliculas
        :return: lista ordenada de cantidad de peliculas por director
        """
        return Etl.counters_sing("director_name",0,list)


    @classmethod
    def ranking_actores(cls, list):
        """
        Utiliza un comprehension para crear una lista que
        es el resultado de la concatenacion de tres listas.
        Esta unica lista tiene todas las apariciones del actor ya sea
        como principal, secundario o terciario.
        Crea un diccionario y lo completa con la estructura de datos.
        Recorre el diccionario agregando al indice (nombre de actor)
        la cantidad de seguidores en FB y la cantidad de peliculas en la que aparecio
        con un +=1, luego verifica si el valor del registro actual en
        el indice IMDB_SCORE es mayor al de comparacion, de ser asi reemplaza pelicula y score.
        Finalmente devuelve un ranking ordenado por IMDB_SCORE.
        :param list: lista de peliculas
        :return: ranking de actor, su mejor pelicula con puntuacion y cantidad de peliculas actuadas
        """
        consolidado = [[row["movie_title"].replace("\xa0", "").strip(), row["actor_"+str(x)+"_name"],row["imdb_score"], int(row["actor_"+str(x)+"_facebook_likes"])] for x in range(1,4) for row in list if len(row["actor_"+str(x)+"_name"])>0]
        actores = {}

        for row in sorted(consolidado,key=lambda x:x[1]):
            actores.update({row[1]:{"BEST_SCORE": 0,"SOCIAL_MEDIA":0,"MOVIE": "","MOVIE_APPEARED": 0}})

        for row in sorted(consolidado,key=lambda x:x[1]):
            actores[row[1]]["SOCIAL_MEDIA"] = row[3]
            actores[row[1]]["MOVIE_APPEARED"] += 1
            if float(actores[row[1]]["BEST_SCORE"]) < float(row[2]):
                actores[row[1]]["MOVIE"] = row[0]
                actores[row[1]]["BEST_SCORE"]=row[2]

        return sorted([[key, value["MOVIE_APPEARED"],value["SOCIAL_MEDIA"],value["MOVIE"],value["BEST_SCORE"]] for key, value in actores.items()],key=lambda x : x[1],reverse=True)

    #METODO DE TAG_CLOUD
    @classmethod
    def tag_cloud(cls,list):
        """
        Utiliza un comprehension para hacer un split del indice de las plot_keywords, luego
        hace la funcion Counter para esta sublista generando un diccionario con word y apariciones.
        Finalmente genera una lista y la devuelve con el peso de las palabras.

        :param list: lista de peliculas
        :return: lista con cantidad de "plot_keywords" y veces que aparecen
        """
        return sorted([[key,value] for key,value in Counter([row_2[x] for row_2 in [row[0].split("|") for row in Etl.analysis_data_sing("plot_keywords",list) if len(row[0])>0] for x in range(len(row_2))]).items()],key=lambda x:x[1],reverse=True)

    @classmethod
    def recaudacion_anual(cls,list,mayor_menor):
        """
        Utiliza una comprehension de 3 indices para traer gross, año y un split del indice genero,
        este comprehension crea una sublista donde recorre len(genero) por cada registro traido
        en el cual la lista final tiene año, genero (unico), gross.
        Se inicializan os diccionarios, uno para ranking y otro de años.
        En el diccionaro de ranking utilizando el indice de tupla año/genero se hace una suma de todos los gross.
        Se hace una comparacion entre el diccionario cargado ranking y el diccionario de entrada years donde se va
        guardando el genero con mayor gross en comparacion a todos los de ese año si el parametro es "mayor" o el
        de menor gross si el parametro es "menor".
        Finalmente se genera una lista sorteada por año de manera creciente.
        :param list: lista de peliculas
        :param mayor_menor: parametro de entrada "mayor" o "menor"
        :return: Lista por año del genero con mayor gross y su valor acumulado
        """
        consolidado = sorted(
            [[row_2[0],row_2[1],row_2[2][x]]for row_2 in [[row["gross"], row["title_year"],row["genres"].split("|")] for row in list if len(row["gross"]) > 0 and len(row["title_year"])>0] for x in  range(len(row_2[2]))],
            key=(lambda x: x[1]))

        ranking = {}
        years = {}

        if mayor_menor == "mayor":

            for row in consolidado:
                ranking.update({(row[1],row[2]):0})
                years.update({row[1]:["",0]})

            for row in consolidado:
               ranking[(row[1],row[2])] += int(row[0])

            for key,value in ranking.items():
                if years[key[0]][1]<value:
                    years[key[0]][0]= key[1]
                    years[key[0]][1]= value
        else:

            for row in consolidado:
                ranking.update({(row[1],row[2]):0})
                years.update({row[1]:["",10000000000000000000000000000]})

            for row in consolidado:
               ranking[(row[1],row[2])] += int(row[0])

            for key,value in ranking.items():
                if years[key[0]][1]>value:
                    years[key[0]][0]= key[1]
                    years[key[0]][1]= value

        return sorted([[key, value[0], value[1]] for key, value in years.items()],key=lambda x:x[0])

    @classmethod
    def directores_reputacion(cls,list):
        """
        Se utiliza una comprehension de dos indices sorteada para traer al director
        y todos sus imdb_score.
        Se inicializa un diccionario ranking donde el indice va a ser el director.
        Se recorre la lista consolidado sumando todos los valores del diccionario["director"]
        y un contador de cantidad de registros, luego se hace la division de promedio.
        Se genera una lista con Director y Mayor promedio IMDB
        :param list: Lista de peliculas
        :return: Ranking top 5 de directores con mejor promedio de IMDB_SCORE
        """
        consolidado =  sorted([[row["director_name"], row["imdb_score"]] for row in list if len(row["imdb_score"])>0 and len(row["director_name"])>0],key=(lambda x: x[1]))

        ranking = {}

        for row in consolidado:
            ranking.update({row[0]:[0,0]})

        for row in consolidado:
            ranking[row[0]][0]+=float(row[1])
            ranking[row[0]][1]+=1

        return sorted([[key,value[0]/value[1]] for key,value in ranking.items()],key=lambda x:x[1],reverse=True)[:5]

    @classmethod
    def mas_gustados(cls,list):
        """
        Se genera una lista de dos indices con un split de generos para formar cantida de gross por genero.
        Se inicializa un diccionario por genero.
        Se hace una sumatoria acumulada por el indice "genre".
        Se genera una lista con genero y gross ordenada de manera decreciente
        :param list: lista de peliculas
        :return: Valor mas alto de gross de todos los generos.
        """
        consolidado = [[ row_2[0], row_2[1][x]] for row_2 in [[row["gross"], row["genres"].split("|")] for row in list if len(row["gross"]) > 0] for x in range(len(row_2[1]))]

        ranking = {}

        for row in consolidado:
            ranking.update({row[1]:0})

        for row in consolidado:
            ranking[row[1]]+=int(row[0])

        return sorted([[key,value] for key,value in ranking.items()],key=lambda x:x[0],reverse=True)[:1]

    @classmethod
    def ejecucion(cls,file_name):
        """
        Funcion de ejecucion de todas las funciones, devuelve
        utilizando generadores de lista de listas con todos
        los parametros

        :param file_name: nombre de archivo a procesar
        :return: Lista de listas con la informacion procesada
        """
        start_time = time.time()

        movie_list = Etl.load_file(file_name)

        yield(Etl.color_bn(movie_list))
        yield(Etl.menos_criticadas(movie_list))
        yield(Etl.mayor_duracion(movie_list))
        yield(Etl.mayor_dinero(movie_list))
        yield(Etl.menor_dinero(movie_list))
        yield(Etl.mayor_presupuesto(movie_list))
        yield(Etl.menor_presupuesto(movie_list))
        yield(Etl.mayor_produccion(movie_list))
        yield(Etl.menor_produccion(movie_list))
        yield(Etl.pelicula_por_director(movie_list))
        yield(Etl.ranking_actores(movie_list))
        yield(Etl.tag_cloud(movie_list))
        yield(Etl.recaudacion_anual(movie_list,"mayor"))
        yield(Etl.recaudacion_anual(movie_list,"menor"))
        yield(Etl.directores_reputacion(movie_list))
        yield (Etl.mas_gustados(movie_list))

        yield('\nTiempo de Ejecucion:{0}'.format(time.time() - start_time))

#MAIN DE PRUEBA DE LA CLASE
if __name__ == "__main__":

    list = Etl.ejecucion();
    for row in list:
        print(row)