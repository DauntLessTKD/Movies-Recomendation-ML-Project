# Importing needed libraries and frameworks

from fastapi import FastAPI
import pandas as pd
import uvicorn
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity


# Making an object of the FastAPI framework
app = FastAPI()


# Making the dataframe using and url of google drive
url = 'https://drive.google.com/file/d/1yxJ3Sm8_CLuDdcMHO5Yuh1POz7Id9lCM/view?usp=sharing'
url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]

df_origin = pd.read_csv(url, dtype={'column_name': str}, low_memory=False)


# Making a welcome message
@app.get("/")
async def menu():

    menu = {'URL API Documentation': '/docs',
            'URL API Funcion 1': '/cantidad/filmaciones/mes/{mes}',
            'URL API Funcion 2': '/cantidad/filmaciones/dia/{dia}',
            'URL API Funcion 3': '/score/titulo/{titulo}',
            'URL API Funcion 4': '/votos/titulo/{titulo}',
            'URL API Funcion 5': '/get/actor/{actor}',
            'URL API Funcion 6': '/get/director/{director}',
            'URL API Funcion 7': '/recomendations/{titulo}'
            }

    return menu


# Function 1: returning the amount of movies in a specific month
@app.get("/cantidad/filmaciones/mes/{mes}")
async def cantidad_filmaciones_mes(mes: str):

    df_origin['release_date'] = pd.to_datetime(df_origin['release_date'])

    # checking if the month is a number
    if mes.isdigit():
        mes_num = int(mes)
        cantidad = df_origin[df_origin['release_date'].dt.month == mes_num].shape[0]

    else:
        # Transforming the month name into lowercase and checking wich month is
        mes = mes.lower()
        meses_nombres = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

        if mes in meses_nombres:
            mes_num = meses_nombres.index(mes) + 1
            cantidad = df_origin[df_origin['release_date'].dt.month == mes_num].shape[0]

        else:
            return {"Error": "El mes ingresado no es válido"}

    return {"Mes": mes, "Cantidad de filmaciones en el mes": cantidad}


# Function 2: returning the amount of movies in a specific day
@app.get("/cantidad/filmaciones/dia/{dia}")
async def cantidad_filmaciones_dia(dia: str):
    df_origin['release_date'] = pd.to_datetime(df_origin['release_date'])

    # Checking if the day is a number
    if dia.isdigit():
        dia_num = int(dia)

    else:
        # Transforming the day name into lowercase and checking wich day is
        dia = dia.lower()
        dias_nombres = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']

        if dia in dias_nombres:
            dia_num = dias_nombres.index(dia) + 1

        else:
            return {"Error": "El día ingresado no es válido"}

    cantidad = df_origin[df_origin['release_date'].dt.day == dia_num].shape[0]

    return {"Día": dia, "Cantidad de filmaciones en el día": cantidad}


# Function 3: returning the release year and popularity for the entered title
@app.get("/score/titulo/{titulo}")
async def score_titulo(titulo: str):

    titulo = titulo.lower()
    peliculas = df_origin[df_origin['title'].str.lower().str.contains(titulo)]
    if peliculas.empty:
        return {"Error": "Película no encontrada"}
    else:
        return peliculas[['title', 'release_year', 'popularity']].to_dict('records')


# Function 4: returning the Title, release year, vote count and vote average
# for the entered title
@app.get("/votos/titulo/{titulo}")
async def votos_titulo(titulo: str):

    titulo = titulo.lower()
    peliculas = df_origin[df_origin['title'].str.lower() == titulo]

    if peliculas.empty:
        return {"Error": "Película no encontrada"}

    else:
        pelicula = peliculas.iloc[0]

        if pelicula['vote_count'] < 2000:
            return {"Error": "La película  no tiene suficientes votos"}

        else:
            return peliculas[['title', 'release_year', 'vote_count','vote_average']].to_dict('records')


# Function 5: returning the name of the entered actor
# his total return value , total amount of movies and return average
@app.get("/get/actor/{actor}")
async def get_actor(actor: str):

    # Asegúrate de que tu columna de actores esté en un formato que puedas filtrar por actor
    peliculas_actor = df_origin[df_origin['cast'].str.contains(actor, na=False)]

    if peliculas_actor.empty:
        return {"Error": "Actor no encontrado"}

    else:
        retorno_total = peliculas_actor['return'].sum()
        cantidad_peliculas = peliculas_actor.shape[0]
        retorno_promedio = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0
        return {"Actor/Actress": actor,"Retorno total": retorno_total, "Cantidad de películas": cantidad_peliculas, "Retorno promedio": retorno_promedio}


# Function 6: returning the name of the director
# his total return value, with all of the movies that work in
@app.get("/get/director/{director}")
async def get_director(director: str):

    peliculas_director = df_origin[df_origin['crew'].str.contains(director, na=False)]

    if peliculas_director.empty:
        return {"Error": "Director no encontrado"}

    else:
        resultados = []

        for _, pelicula in peliculas_director.iterrows():
            resultados.append({"Título": pelicula['title'],"Año de lanzamiento": str(pelicula['release_date'][:4]),
                            "Retorno individual": pelicula['return'],"Presupuesto de la pelicula": pelicula['budget'],"Ganancia": pelicula['revenue']})

        retorno_total = peliculas_director['return'].sum()
        return {"Retorno total": retorno_total,"Películas": resultados}


# Filling all the empty values in the column genres
df_origin['genres'] = df_origin['genres'].fillna('')

# Combining two characteristics 'genres' and 'vote_average'
df_origin['features'] = df_origin['genres'].astype(str) + ' ' + df_origin['vote_average'].astype(str)

# Making a TF IDF matrix for the combined characteristics
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df_origin['features'])

# Creating a recomendation function , to use it in the API function
def recomendacion(titulo):

    # Setting the title in lower case
    titulo = titulo.lower()

    # Filtering movies using the title
    pelicula_seleccionada = df_origin[df_origin['title'].str.lower() == titulo]

    if pelicula_seleccionada.empty:
        return []

    # Taking the index of the selected movie
    index = pelicula_seleccionada.index[0]

    # Finding the similarity between movies using combined characteristics
    similarity_scores = cosine_similarity(tfidf_matrix[index], tfidf_matrix)

    # Finding the indexes of the more similar movies
    similar_movies_indices = similarity_scores.argsort()[0][-5:][::-1]

    # Finding the titles and vote_average of the most similar movies
    peliculas_similares = df_origin.iloc[similar_movies_indices][['title', 'vote_average']].values.tolist()

    # Sorting the movies using the score in a descending order
    peliculas_similares = sorted(peliculas_similares, key=lambda x: x[1], reverse=True)

    # Setting movies in the returned list if needed
    while len(peliculas_similares) < 5:
        peliculas_similares.append(['Película adicional', 0])

    return peliculas_similares


# Function 7: Using the recomendation model to find the most similar movies
@app.get("/recomendations/{titulo}")
async def obtener_recomendacion(titulo: str):

    recomendaciones = recomendacion(titulo)

    if len(recomendaciones) == 0:
        return {"Error": "Película no encontrada"}

    else:
        return {"Recomendaciones": recomendaciones}


# Needed for reloading the API response live time
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)