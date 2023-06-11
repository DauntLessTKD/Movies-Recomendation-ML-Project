# Movies-Recomendation-ML-Project

Overwiev

The problem presented in this project is to create an API in which there is a Machine Learning Model together with 6 functions which will be detailed in the next paragraphs.

in the file 'PI_1_ETL.ipynb'
there is the ETL process of the csv used in the project, notebook in which everything is documented step by step in detail

in the File
'PI_1_EDA.ipynb'
We can see some methods and graphs, which guide us to be able to develop the recommendation model in an optimal way.

in the File
'main.py' is our API created with the needed documentation

Menu:

To enter in the documentation: URL/docs

To use the endpoints at the end of the url , you should enter

the data you want to process.

Next to this i will put all the URL for the functions:

Quantity of movies per month:  URL/cantidad_filmaciones_mes/{mes}

Quantity of movies per month:
URL/cantidad_filmaciones_dia/{dia}

Score of a movie:
URL/score_titulo/{titulo}

Votes obtained by a movie
URL/votos_titulo/{titulo}

Get an Actor in our Data
URL/get_actor/{nombre_actor}

Get an Director in our Data
URL /get_director/{nombre_director}

Get 5 similar movies recomende by our ML Model
URL/recomendacion/{titulo}
