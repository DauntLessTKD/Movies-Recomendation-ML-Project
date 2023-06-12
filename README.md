**Movies Recomendation ML Project**

![Project Image](https://drive.google.com/file/d/1cDpWvtHoG8rSOwbBnXDiU9k-raDOUJLd/view?usp=sharing)

 *Recomendation ML* The user will have to provide a movie that he watched, and our ML model will recomend him a list of movies
 that are similar to the user given movie, just like netflix or youtube, this model can recomend similar content to the user
 based on their preferences.

## 📋 Table of Contents

1. [Extract , Transform and Load, ETL Process](#ETL)
2. [Exploratory Data Analysis](#EDA)
3. [Recommendation Model](#MLModel)
4. [Manual of ussage](#use)
5. [DOCS Endpoints](#DOCSendpoint)
6. [Libraries](#Libraries)
7. [License](#license)

## 🧹 1. Extract , Transform and Load, ETL Process `<a name="ETL"></a>`

The first to be done in this project, was this process, the csv files , it has to be extracted into a dataframe, cleaned, transformed
and finally load them into another final csv [See ETL](PI_1_ETL.ipynb)

## 📊 2. Exploratory Data Analysis, EDA Process `<a name="EDA"></a>`

After making the ETL process, we see the data in a more detailed way using graphics, to be able making the API  [See EDA](PI_1_EDA.ipynb)

## 🎯 3. Recommendation Model `<a name="MLModel"></a>`

Using the ETL and EDA process for be able, to create the functions and the ML recomendation model in an optimal way
doing the use of libraries like TF IDF, Cosine-similarity, to be able getting similar movies like the input one [See API-ML](main.py)

## 💡 4. Manual of ussage `<a name="use"></a>`

When the user clicks on documentation links or URL, they will have to click on the blue "GET" buttom of the function that they want to
execute , after that click on the buttom "try it out", then put your input in the box below , after this click on "execute", you will se the result wanted below that "execute" buttom

If you go directly to a functions endpoint, you will have to put your input before the URL like this:
endpoint URL/"user input"
## 📚 5. DOCS Endpoints `<a name="DOCSendpoint"></a>`

The *Recomendation ML Project* API offers various endpoints that provide unique functionalities for movie data exploration and recommendation generation. Here we describe each of them:

[`documentation`](https://pi-1-rodrigo-escalona.onrender.com/docs): In this URL , you can enter the API documentation, where are all
of the functions in an visual way, that ables the user to interact with the 6 functions that are available and the machine learning model

## ⚙️ 6. Libraries `<a name="Libraries"></a>`

This are the needed libraries and frameworks that allows this project to work correctly.

- pandas
- numpy
- seaborn
- matplotlib
- sklearn
- FastAPI
- Uvicorn
- missingno
- sweetviz
- wordcloud

## 📄 7. License `<a name="license"></a>`

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 2, June 1991.
