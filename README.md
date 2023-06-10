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



Quantity of movies per month:  
URL/cantidad/filmaciones/mes/

Quantity of movies per month:
URL/cantidad/filmaciones/dia/

Score of a movie:
URL/score/titulo/

Votes 

    'URL API Funcion 4': '/votos/titulo/{titulo}',
            'URL API Funcion 5': '/get/actor/{actor}',
            'URL API Funcion 6': '/get/director/{director}',
            'URL API Funcion 7': '/recomendations/{titulo}'
