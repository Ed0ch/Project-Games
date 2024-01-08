

#Cargar todas las librerías
import pandas as pd  
import matplotlib.pyplot as plt 
import numpy as np 
import seaborn as sns 
from scipy import stats as st 
import datetime as dt 


#Preparación de los datos

df_games=pd.read_csv("C:/Users/carlo/OneDrive/Documentos/Project-Games/games.csv") #Cargar el dataset con el que vamos a trabajar

print(df_games.head()) #Imprimimos el dataframe para saber como está organizado y que es lo que contiene.


df_games.columns=df_games.columns.str.lower() #Convertimos el título de las columnas a minúsculas para que sea mas sencillo leerlo
df_games.head() #Imprimimos nuevamente el título de las columnas para ver que los cambios se hayan efectuado.
df_games.info() # Revisar el dataframe para comprobar que información y que tipo de datos tenemos en cada una de las columnas.
df_games['rating']=df_games['rating'].fillna('Unknown') #rellenar con Unknown en rating los valores ausentes
df_games['year_of_release']=pd.to_numeric(df_games['year_of_release'],errors='coerce').astype('Int64') #convertir a entero los años.
df_games['user_score']=pd.to_numeric(df_games['user_score'],errors='coerce') #Convertimos la columna de la calificación de los usuarios a tipo float.

# 'year_of_release ---> Se convirtió a int64 ya que los años son numeros enteros.
# 'critic_score' ---> Se convirtió a int64 ya que los datos estan basados en 100 y no tienen decimales.
# 'user_score' –––> Se convirtió a float64 ya que son numeros y estaban como tipo object.

# Lo que puedo observar es que tenemos algunos valores ausentes en el dataframe. Analizandolo un poco más puedo observar que en el rating hay algunos valores categoricos quer podríamos remplazar por "Unknown".
# Pero en el caso de user score y critic score considero que "rellenar" o "remplazar" esos valores, generaría problemas, ya que en una de esas columas representaría más del 50% de los datos, lo que nos generaría algo completamente distinto si modificamos esos datos, por lo que he llegado a la conclusión de que no realizaré esa modificación.



df_games['total_sales']=df_games['na_sales']+df_games['eu_sales']+df_games['jp_sales']+df_games['other_sales'] #Calcular las ventas totales para cada juego y crear una columna.
print(df_games.head(8))



#Creamos un gráfico por año de lanzamiento
games_by_year=df_games.groupby('year_of_release')['name'].count() #para contar cuantos juegos fueron lanzados por años
games_by_year #me arroja una tabla de 1980 hasta después del 2000 que si sirve pero no la veo tan útil
games_by_year.plot()


# En este caso puedo observar que el lanzamiento de los juegos fueron fue en ascenso conforme el paso de los años, se puede ver una tendencia claramente hacia el alza, siendo del 2005 al 2010 el pico más grande en cuestión de lanzamientos,  de ahi en adelante se ve una clara tendencia a la baja en los lanzamientos.



#Creamos un gráfico para ver las ventas totales por plataforma
platforms=df_games.groupby('platform')['total_sales'].sum() #Agrupar por plataforma y contar el total de ventas

platforms.plot(kind='bar',x='platform',y='total_sales',ylabel='Total sales') #graficar para ver la distribución y analizar cuales son los que más venden.

# Se puede ver con claridad que PS2 lidera en ventas y que X360,PS3,DS también tienen ventas bastantes destacables o muy por encima de las demás plataformas.

#Creamos un gráfico odenado para ver las plataformas de manera ascendente .
platforms_s=platforms.sort_values(ascending=False) #Ordenr las ventas totales por plataforma en orden descendente
platforms_s.plot(kind='bar')
print(platforms_s)
platforms_s.head(8)# Listado de 8 plataformas con más ventas


#Aqui considero que las plataformas con más ventas son las primeras ocho que aparecen en el listado superior.



#Creamos un gráfico de las ventas totales de las  plataformas más populares
df_popular=df_games.groupby('platform')['total_sales'].sum().sort_values(ascending=False).head(8) #agrupar por plataforma en la columna de ventas para ordenar el dataframe
df_years=df_games.pivot_table(index='year_of_release',columns='platform',values='total_sales',aggfunc='sum') #Crear una tabla pivote que nos muestre por columna las ventas por cada año en la distintas plataformas
df_top=df_popular.index.tolist() #crear una lista para poder pasarla al dataframe después
df_top_pivot=df_years[df_top]
df_top_pivot.plot()


# Lo que puedo analizar del gráfico es que la vida util de cada plataforma es de 10 años en promedio, también podemos analizar que por lo general todas tuvieron un pico hasta cierto punto pasados 5 años y de ahi comenzaron su caída.



#Creamos un gráfico de para los juegos que se lanzaron del año 2000 en delante para ver las ventas totales por plataforma.
df_filtered=df_games[df_games['year_of_release']>=2000] #Datos que considero relevantes

df_modelo=df_games[df_games['year_of_release']>2011] #Datos corregidos de años relevantes

df_modelo_ventas=df_modelo.groupby('platform')['total_sales'].sum().sort_values(ascending=False) #Ordener el modelo de datos filttadps

df_modelo_ventas.plot(x='platform',y='total_sales',kind='bar')

# Las plataformas que son líderes en ventas son PS2,WII,X360,PS3,DS,PS4. Siendo PS2  y WII las plataformas que tiene más ventas que las demás,pese a que las otras son bastantes buenas.
# Considero que utilizando estas plataformas podemos trabajar en mejorar el rating de ellas con publicidad y podríamos sacarle más provecho a cada una de las plataformas que se muestran arriba.



df_popular=df_games.groupby('platform')['total_sales'].sum().sort_values(ascending=False).head(8) #crear el dataframe con las 8 plataformas de mayor venta
df_popular.plot(kind='bar',xlabel='Platform',ylabel='Total Sales')

#Creación de diagrama de caja de bigotes para ver las ventas por plataforma

sns.boxplot(data=df_top_pivot) #crear el boxplot para revisar la distribución de esas plataformas
plt.title('Diagrama de caja para ventas por plataforma') 
plt.xlabel('Platform')
plt.ylabel('Total sales')


# Podemos observar que las ventas si son significativas si comparamos las dstintas plataformas, algunas van de ciertos rangos más pequeños y otras más grandes.
# Podemos ver que las ventas promedio si varían de plataforma en plataforma y la mediana de todos los datos a pesar de que en algunos es muy parecida, si tiene diferencias signigficativas, hay algunas distribuciones cargadas a valores pequeños y otras a valores grandes, todas son asimétricas.



#Análsis del PS2 plataforma seleccionada para realizar un análsis más en particular

PS2=df_filtered[df_filtered['platform']=='PS2'] #Seleccionar la plataforma popular de mi elección
PS2.plot(x='critic_score',y='total_sales',kind='scatter',title='Correlación de reseñas vs ventas',xlabel='Critic score',ylabel='Total Sales')


corr=PS2['critic_score'].corr(PS2['total_sales']) #aqui estoy sacando el factor de correlación para corroborar que sea positiva y ver que tan fuerte es
print(corr) 




PS2=df_filtered[df_filtered['platform']=='PS2'] #Seleccionar la plataforma popular de mi elección, que  en este caso será PS2

PS2.plot(x='user_score',y='total_sales',kind='scatter',title='Correlación de reseñas por usuario vs ventas',xlabel='User  Score',ylabel='Total Sales')




corr_user=PS2['user_score'].corr(PS2['total_sales']) #Sacar la correlación para ver que sea positiva y ver que tan fuerte es
print(corr_user)




# En ambos graficos podemos obsevar que hay una correlación positiva acerca del puntuaje que efectuan tanto los profesionales como lo usuarios sobre las ventas, es decir, a mayor puntuaje se ve un impacto positivo en la cantidad de ventas.
# Es más notorio en las calificaciones que dan los profesionales, suele mostrar un buen impacto en el caso del PS2.
# Revisando los datos podemos llegar a la conclusión de que las plataformas con más ventas, como lo son PS2,X360,WII, etc, llegan a tener mayor numero de ventas por que tienen buenas calificaciones en su mayoría, lo que a su vez se traduce en que si se tiene una buena calificación, podríamos esperar que determinado juego en cierta plataforma tenga exito.




genre=df_games.groupby('genre')['total_sales'].mean() #sacar  el promedio de las ventas por género
genre.plot(title='Ventas por género',xlabel='genre',ylabel='Total Sales',kind='bar')


# Revisando los géneros y las ventas promedio, podemos osbervar que lps géneros que destacan muy por encima de los demás son los de plataforma, seguido por los juegos de Shooter y siendo el tercero el genero de juego de rol.
# Podemos osbervar que los generos más bajos van un poco relacionado a la estrategia o el de aventuras.



df_na=df_games[['name','platform','genre','na_sales','year_of_release','critic_score','user_score','rating']] #crear un dataframe solo para  NA
print(df_na)

df_na_platform=df_na.groupby('platform')['na_sales'].sum().sort_values(ascending=False).head(5) #Sacar las ventas por la región NA
df_na_platform.plot(title='Ventas de región NA',x='Platforms',y='NA Sales',kind='bar')

df_na_genre=df_na.groupby('genre',)['na_sales'].sum().sort_values(ascending=False).head(5)
df_na_genre.plot(title='Ventas por género en la región NA',xlabel='Genres',ylabel='Total_sales',kind='bar')


df_na_rating=df_na.groupby('rating')['na_sales'].sum() #sacar el total de ventas por rating
df_na_rating.plot(title='Ventas por rating',xlabel='Rating',ylabel='Ventas en la región NA',kind='bar') #Creación de gráfico de ventas por rating





df_eu=df_games[['name','platform','genre','eu_sales','year_of_release','critic_score','user_score','rating']] #Crear un dataframe para EU
df_eu_platform=df_eu.groupby('platform')['eu_sales'].sum().sort_values(ascending=False).head(5) #Saque las ventas por plataforma en la región EU
df_eu_platform.plot(title='Ventas de región EU',x='Platforms',y='EU Sales',kind='bar')

df_eu_genre=df_eu.groupby('genre')['eu_sales'].sum().sort_values(ascending=False).head(5) #Crear el dataframe para verlo por género en la región EU
df_eu_genre.plot(title='Ventas por género en la región EU',x='Platforms',y='EU Sales',kind='bar')

df_eu_rating=df_eu.groupby('rating')['eu_sales'].sum() #Crer esta para verlo por rating
df_eu_rating.plot(title='Ventas por rating',xlabel='Rating',ylabel='Ventas en la región EU',kind='bar')


df_jp=df_games[['name','platform','genre','jp_sales','year_of_release','critic_score','user_score','rating']] #creo un dataframe solo para el JP

df_jp_platform=df_jp.groupby('platform')['jp_sales'].sum().sort_values(ascending=False).head(5) #Cree el dataframe jp para verlo por plataforma
df_jp_platform.plot(title='Ventas de región JP',x='Platforms',y='JP Sales',kind='bar')

df_jp_genre=df_jp.groupby('genre')['jp_sales'].sum().sort_values(ascending=False).head(5) #cree el dataframe para verlo por género
df_jp_genre.plot(title='Ventas por género de región JP',x='Platforms',y='JP Sales',kind='bar')

df_jp_rating=df_jp.groupby('rating')['jp_sales'].sum() #Cree para verlo por rating
df_jp_rating.plot(title='Ventas por rating',xlabel='Rating',ylabel='Ventas en la región JP por rating',kind='bar')


# Si revisamos los perfiles de cada región podemos darnos cuenta principalmente hay una plataforma distinta que predomina para cada región y que esas plataformas coinciden con las que más demanda tiene si nos vamos más arriba con las principales que más venden.
# También podemos concluir que los géneros que más se juegan sería acción y deportes en su mayoría.
# Si considero que el rating afecta las ventas, ya que hay juegos de calsificación "E" que suelen ser de los más vendidos. 
# Un punto a destacar muy importante es que las regiones EU y NA a pesar de que tienen ciertas similitudes en sus comportamientos, son distintas pero la región JP es bastante distinta si comparamos los comportamientos de las demás regiones.



df_xone=df_games[df_games['platform']=='XOne'] #crear el dataframe que me seleccione solo xbox one
df_xone=df_xone.dropna(subset=['user_score']) #si metemos valores NAN a la prueba de hipotesis no nos dará nada, por lo que hay que quitarlos en esta parte
media_xone=df_xone['user_score']



df_pc=df_games[df_games['platform']=='PC'] #crear el dataframe para la PC
df_pc=df_pc.dropna(subset=['user_score'])
media_pc=df_pc['user_score']

# En esta parte lo unico que estoy haciendo es filtar los datos para poder testear acá abajo las hipotésis.



# ## Prueba de Hipótesis de XONE y PC

# Para la prueba de hipotesis tomaremos las muestras de las calificaciones de lo usuarios de las plataformas de XONE y de PC, consideraremos la varianzas iguales y realizaremos la prueba de la siguiente manera: 
# H0= No hay diferencia significativa entre las calificaciones de los usuarios.
 
# H1= Hay una diferencia significativa entre las calificaciones de los usuarios.




#Realizaremos una prueba de levene para las varianzas de XONE Y PC
#Hipótesis nula (H0): La varianza de los dos grupos es igual.

#Hipótesis alternativa (H1): La varianza de al menos uno de los grupos es diferente.

variance_test_1=st.levene(media_xone,media_pc)
variance_test_1.statistic

alpha=0.05
if variance_test_1.pvalue < alpha:
     print('Rechazamos la hipótesis nula') 
else:
    print('No podemos rechazar la hipótesis nula') 
    


# Eso nos indica que no hay evidencia suficiente para afirmar que las varianzas son diferentes entre las plataformas de Xbox one y PC.


alpha=0.05

results=st.ttest_ind(media_xone,media_pc,equal_var=True)

print('valor p',results.pvalue)

if results.pvalue < alpha:
    print('Rechazamos la hipótesis nula') 
else:
    print('No podemos rechazar la hipótesis nula') 
    
    

# ## Resultado 
# Al rechazar la hipotesis nula podemos concluir que hay diferencias significativas en las calificaciones que los usuarios dejan en las plataformas, es decir, las calificaciones tienen diferencias si es que se juegan en una plataforma u la otra.
# 


# Prueba de Hipotésis para géneros de Acción y Deportes
# 
# Para la prueba de hipotesis tomaremos las muestras de las calificaciones de lo usuarios asignadas por género de Acción y de Deportes , consideraremos la varianzas iguales y realizaremos la prueba de la siguiente manera:
# 
# H0= No hay diferencia significativa entre las calificaciones de los usuarios entre los géneros de Acción y de Deportes
# 
# H1= Hay una diferencia significativa entre las calificaciones de los usuarios entre los géneros de Acción y de Deportes




df_action=df_games[df_games['genre']=='Action'] #Se crean los filtros para realizar el filtrado por género y el más jugado
df_action=df_action.dropna(subset=['user_score'])
media_action=df_action['user_score']

df_sports=df_games[df_games['genre']=='Sports']
df_sports=df_sports.dropna(subset=['user_score'])
media_sports=df_sports['user_score']





#Realizaremos una prueba de levene para las varianzas del genero Action y Sports.
#Hipótesis nula (H0): La varianza de los dos grupos es igual.

#Hipótesis alternativa (H1): La varianza de al menos uno de los grupos es diferente.


variance_test_2=st.levene(media_action,media_sports) #Prueba de levene para la comparación de las medias action y sports
variance_test_2.statistic

alpha=0.05
if variance_test_2.pvalue < alpha:
     print('Rechazamos la hipótesis nula') 
else:
    print('No podemos rechazar la hipótesis nula') 


# Por lo que concluimos que las varianzas no son iguales




alpha=0.05

results=st.ttest_ind(media_action,media_sports,equal_var=False)

print('valor p',results.pvalue)

if results.pvalue < alpha:
    print('Rechazamos la hipótesis nula') 
else:
    print('No podemos rechazar la hipótesis nula') 
    



# ## Resultado  
# 
# Al no poder rechazar la hipotesis nula podemos concluir de que no hay evidencia suficiente para afirmar de que existen diferencias significativas, por lo que podemos decir que las calificaciones de acción y deportes no tiene diferencias significativas en las calificaciones dadas por usuarios.
# 

# Para finalizar el proyecto puedo concluir que realmente el manejo de datos es super importante para realizar un análisis a lo largo de todas las pruebas y visualizaciones que podemos hacerle a un dataset.
# Conforme fui avaznando me di cuenta de que realmente hay relevancia en prestar atención a las plataformas que selecciones, creo que si le invierte uno en publicidad para mejorar las calificaciones, podrías generar más ventas aun en aquellas plataformas  que no tienen tantas ventas y en las que sí podríamos maximizar las califaciones.
# Un factor que también contibuye bastante y que puede ayudar a mejorar las ventas en las distintas plataformas, es la de conseguir más juegos de acción o enfocarse más en ellos, ya que muestra significativa relevancia en las ventas, y considero que con el manejo adecuado puedo conseguir uno potencializar más las ventas.
# 
# 


