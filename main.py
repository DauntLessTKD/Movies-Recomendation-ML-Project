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


# Making the dataframe using the url of google drive
url = 'https://drive.google.com/file/d/1Px4Ufyb6m-o2E_4oefNyVjCrXvv2GiZQ/view?usp=sharing'
url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]

df_origin = pd.read_csv(url, dtype={'column_name': str}, low_memory=False)


# Function 1: returning the amount of movies in a specific month
@app.get("/cantidad_filmaciones_mes/{mes}")
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

    return {"mes": mes, "cantidad": cantidad}


# Function 2: returning the amount of movies in a specific day
@app.get("/cantidad_filmaciones_dia/{dia}")
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

    return {"dia": dia, "cantidad": cantidad}


# Function 3: returning the release year and popularity for the entered title
@app.get("/score_titulo/{titulo}")
async def score_titulo(titulo: str):

    titulo = titulo.lower()
    peliculas = df_origin[df_origin['title'].str.lower().str.contains(titulo)]

    if peliculas.empty:
        return {"Error": "Película no encontrada"}

    else:
        resultado = {'titulo': peliculas['title'],
                    'anio': peliculas['release_year'],
                    'popularidad': peliculas['popularity']}
        return resultado


# Function 4: returning the Title, release year, vote count and vote average
# for the entered title
@app.get("/votos_titulo/{titulo}")
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
            resultado = {'titulo': peliculas['title'],
                        'anio': peliculas['release_year'],
                        'voto_total': peliculas['vote_count'],
                        'voto_promedio': peliculas['vote_average']}
        return resultado


# Function 5: returning the name of the entered actor
# his total return value , total amount of movies and return average
@app.get("/get_actor/{nombre_actor}")
async def get_actor(nombre_actor: str):

    # Asegúrate de que tu columna de actores esté en un formato que puedas filtrar por actor
    peliculas_actor = df_origin[df_origin['cast'].str.contains(nombre_actor, na=False)]

    if peliculas_actor.empty:
        return {"Error": "Actor no encontrado"}

    else:
        retorno_total = peliculas_actor['return'].sum()
        cantidad_peliculas = peliculas_actor.shape[0]
        retorno_promedio = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0
        return {"actor": nombre_actor, "cantidad_filmaciones": cantidad_peliculas,"retorno_total": retorno_total, "retorno_promedio": retorno_promedio}


# Function 6: returning the name of the director
# his total return value, with all of the movies that work in
@app.get("/get_director/{nombre_director}")
async def get_director(nombre_director: str):

    peliculas_director = df_origin[df_origin['crew'].str.contains(nombre_director, na=False)]

    if peliculas_director.empty:
        return {"Error": "Director no encontrado"}

    else:
        resultados = []

        for _, pelicula in peliculas_director.iterrows():
            resultados.append({"titulo": pelicula['title'],"anio": str(pelicula['release_date'][:4]),
                            "retorno_pelicula": pelicula['return'],"budget_pelicula": pelicula['budget'],"revenue_pelicula": pelicula['revenue']})

        retorno_total = peliculas_director['return'].sum()
        return {"director":nombre_director ,"retorno_total_director": retorno_total,"peliculas": resultados}


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

    return peliculas_similares


# Function 7: Using the recomendation model to find the most similar movies
@app.get("/recomendacion/{titulo}")
async def obtener_recomendacion(titulo: str):

    recomendaciones = recomendacion(titulo)

    if len(recomendaciones) == 0:
        return {"Error": "Película no encontrada"}

    else:
        return {"lista_recomendada": recomendaciones}



# Combining two characteristics 'genres' and 'vote_average' and 'overview'
df_origin['features'] = df_origin['genres'].astype(str) + ' ' + df_origin['vote_average'].astype(str) + ' ' + df_origin['overview'].astype(str)

# Making a TF IDF matrix for the combined characteristics
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df_origin['features'])

# Creating a recomendation function , to use it in the API function
def recomendacion2(titulo):

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
    peliculas_similares = df_origin.iloc[similar_movies_indices][['title', 'vote_average','ovreview']].values.tolist()

    # Sorting the movies using the score in a descending order
    peliculas_similares = sorted(peliculas_similares, key=lambda x: x[1], reverse=True)

    return peliculas_similares


# Function 7: Using the recomendation model to find the most similar movies
@app.get("/recomendacion2/{titulo}")
async def obtener_recomendacion(titulo: str):

    recomendaciones = recomendacion2(titulo)

    if len(recomendaciones) == 0:
        return {"Error": "Película no encontrada"}

    else:
        return {"lista_recomendada": recomendaciones}




# Needed for reloading the API response in live time
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)