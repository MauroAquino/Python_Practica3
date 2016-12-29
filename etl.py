import csv
import time
from collections import Counter


class Etl:

    #METODO PARA TRAER TODOS LOS REGISTROS, SE UTILIZA UN SET PARA ELIMINAR REGISTROS DUPLICADOS
    @classmethod
    def load_file(cls, file_name):
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

    #METODO PARA TRAER LOS CONTADORES POR TIPO DE PELICULA
    @classmethod
    def color_bn(cls,list):

        #PELICULAS COLOR BN Y VACIAS
        def color_bn_traer(param):
            return len([row['movie_title'] for row in list if row['color'].strip() == param])

        return {'Color':color_bn_traer("Color"),'Blanco y Negro' : color_bn_traer("Black and White"), 'Vacio' : color_bn_traer("")}

    #METODO DE ANALISIS DE INFORMACION EN BASE A DOS INDICES
    @classmethod
    def analysis_data_doub(cls,param_uno,param,list):

        return sorted([[row[param_uno].replace("\xa0", "").strip(), int(row[param])] for row in list if len(row[param])>0],key=(lambda x: x[1]))

    #METODO DE ANALISIS DE INFORMACION EN BASE A UN INDICE
    @classmethod
    def analysis_data_sing(cls, param_uno, list):

        return sorted(
            [[row[param_uno].replace("\xa0", "").strip()] for row in list],key=(lambda x: x[0]))

    #METODO DE CONTADOR DE LISTA EN BASE A DOS INDICES
    @classmethod
    def counters_doub(cls, param_uno, param, param_dos, list):

        return sorted([[key, value] for key, value in Counter([a[param_dos] for a in Etl.analysis_data_doub(param_uno, param, list)]).items()], key=lambda x: x[1])

    #METODO DE CONTADOR DE LISTA EN BASE A UN INDICE
    @classmethod
    def counters_sing(cls, param_uno, param_dos, list):

        return sorted([[key, value] for key, value in Counter([a[param_dos] for a in Etl.analysis_data_sing(param_uno, list)]).items()],key=lambda x: x[1])

    #METODOS DE CLASE PARA TRAER CADA UNO DE LOS PUNTOS
    @classmethod
    def menos_criticadas(cls,list):

        return Etl.analysis_data_doub("movie_title","num_critic_for_reviews",list)[:10]

    @classmethod
    def mayor_duracion(cls, list):

        return Etl.analysis_data_doub("movie_title", "duration", list)[-20:]

    @classmethod
    def mayor_dinero(cls, list):

        return Etl.analysis_data_doub("movie_title", "gross", list)[-5:]

    @classmethod
    def menor_dinero(cls, list):

        return Etl.analysis_data_doub("movie_title", "gross", list)[:5]

    @classmethod
    def mayor_presupuesto(cls, list):

        return Etl.analysis_data_doub("movie_title", "budget", list)[-3:]

    @classmethod
    def menor_presupuesto(cls, list):

        return Etl.analysis_data_doub("movie_title", "budget", list)[:3]

    @classmethod
    def mayor_produccion(cls, list):

       return Etl.counters_doub("movie_title","title_year",1,list)[-1:]

    @classmethod
    def menor_produccion(cls, list):

       return Etl.counters_doub("movie_title","title_year",1,list)[:1]

    @classmethod
    def pelicula_por_director(cls, list):

       return Etl.counters_sing("director_name",0,list)

    #METODO DE RANKING DE ACTORES
    @classmethod
    def ranking_actores(cls, list):

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

        return sorted([[key,value] for key,value in Counter([row_2[x] for row_2 in [row[0].split("|") for row in Etl.analysis_data_sing("plot_keywords",list) if len(row[0])>0] for x in range(len(row_2))]).items()],key=lambda x:x[1],reverse=True)

    @classmethod
    def recaudacion_anual(cls,list,mayor_menor):

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
                years.update({row[1]:["",1000000000000000000]})

            for row in consolidado:
               ranking[(row[1],row[2])] += int(row[0])

            for key,value in ranking.items():
                if years[key[0]][1]>value:
                    years[key[0]][0]= key[1]
                    years[key[0]][1]= value

        return sorted([[key, value[0], value[1]] for key, value in years.items()],key=lambda x:x[0])





if __name__ == "__main__":

    start_time = time.time()
    movie_list = Etl.load_file("movie_metadata.csv")

    print(Etl.color_bn(movie_list))
    print(Etl.menos_criticadas(movie_list))
    print(Etl.mayor_duracion(movie_list))
    print(Etl.mayor_dinero(movie_list))
    print(Etl.menor_dinero(movie_list))
    print(Etl.mayor_presupuesto(movie_list))
    print(Etl.menor_presupuesto(movie_list))
    print(Etl.mayor_produccion(movie_list))
    print(Etl.menor_produccion(movie_list))
    print(Etl.pelicula_por_director(movie_list))
    print(Etl.ranking_actores(movie_list))
    print(Etl.tag_cloud(movie_list))
    print(Etl.recaudacion_anual(movie_list,"mayor"))
    print(Etl.recaudacion_anual(movie_list,"menor"))

    print('\nTiempo de Ejecucion:{0}'.format(time.time()-start_time))