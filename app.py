import streamlit as st
import pandas as pd
from sklearn.datasets import fetch_california_housing

st.title("Análisis de Viviendas en California")

#Cargar dataset
california = fetch_california_housing()

#Crear el dataframe
df_california = pd.DataFrame(california.data, columns=california.feature_names)

#Agregar la variable
df_california["MedHouseVal"] = california.target

#Mostrar las primeras 5 filas
st.header("Top 5 filas del dataset")
st.dataframe(df_california.head())

#Mostrar tipo de dato
st.header("Tipo de datos")
st.write(df_california.dtypes.astype(str))

#Barra lateral para filtros
st.sidebar.markdown("## Filtros de Viviendas")
st.sidebar.markdown("Utilizá los siguientes filtros para explorar los datos de California")

#Obtener la edad mínima y máxima
edad_min = int(df_california["HouseAge"].min())
edad_max = int(df_california["HouseAge"].max())

#Crear el filtro por antigüedad
rango_edad = st.sidebar.slider("Antiüedad de las viviendas",
                               min_value=edad_min,
                               max_value=edad_max,
                               value=(edad_min, edad_max)
                               )

#Filtrar los datos según la antigüedad seleccionada
df_filtrado = df_california[
    (df_california["HouseAge"] >= rango_edad[0]) &
    (df_california["HouseAge"] <= rango_edad[1])
]

#Filtrar por latitud mínima
latitud_min = st.sidebar.number_input(
    "Latitud mínima",
    min_value=float(df_california["Latitude"].min()),
    max_value=float(df_california["Latitude"].max()),
    value=float(df_california["Latitude"].min())
)

#Filtrar los datos por antigüedad y latitud
df_filtrado = df_california[
    (df_california["HouseAge"] >= rango_edad[0]) &
    (df_california["HouseAge"] <= rango_edad[1]) &
    (df_california["Latitude"] >= latitud_min)
]

#Mostrar los datos filtrados
st.header("Viviendas filtradas")
st.dataframe(df_filtrado)

#Resumir los datos filtrados
if not df_filtrado.empty:
    mediana = df_filtrado["MedHouseVal"].max()
    rango = (
        df_filtrado["MedHouseVal"].max()
        - df_filtrado["MedHouseVal"].min()
    )

    st.header("Resumen descriptivo")
    st.write("Mediana del valor de las viviendas:", mediana)
    st.write("Rango del valor de las viviendas:", rango)
else:
    st.write("No hay datos para los filtros seleccioandos.")

import matplotlib.pyplot as plt

#Crear histograma de valores de viviendas
st.header("Distribución del valor de las viviendas")

if not df_filtrado.empty:
    fig, ax = plt.subplots()

    ax.hist(df_filtrado["MedHouseVal"], bins=30)

    ax.set_title("Histograma de valores de las viviendas")
    ax.set_xlabel("Valores de las viviendas (cientos de miles de USD)")
    ax.set_ylabel("Frecuencia")

    st.pyplot(fig)
    plt.close(fig)

#Crear gráfico de dispersión
st.header("Relación entre ingresos y valor de las viviendas")

if not df_filtrado.empty:
    fig, ax = plt.subplots()

    ax.scatter(
        df_filtrado["MedInc"],
        df_filtrado["MedHouseVal"],
        alpha=0.5,
    )
    ax.set_title("Ingresos vs. Valor de las viviendas")
    ax.set_xlabel("Mediana de ingresos (decenas de miles de USD)")
    ax.set_ylabel("Valor mediano de las viviendas (cientos de miles de USD)")

    st.pyplot(fig)
    plt.close(fig)

#Mapa geografico de los datos filtrados
st.header("Distribución geográfica de las viviendas")

if not df_filtrado.empty:
    st.map(
        df_filtrado,
        latitude="Latitude",
        longitude="Longitude",
    )