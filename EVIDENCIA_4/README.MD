Dashboard LogiMayab – Equipo Pi-Thon's
Integrantes del Equipo

Iker Villalobos Gilling – A01710453

Juan Carlos Cárcamo Alarcón – A01710253

José David Castillo Jasso – A01710953

Ana Isabel García Mojica – A01706241

Presentación Final

Puedes consultar la presentación del proyecto en el siguiente enlace:
https://www.canva.com/design/DAG6eULcP2Q/_UzpQETJNqceFTnYF44EUg/edit?utm_content=DAG6eULcP2Q&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

Descripción General

El proyecto LogiMayab Dashboard es una aplicación web interactiva diseñada para visualizar indicadores clave de operación, costos, rutas, desempeño y estado de riesgo mediante técnicas de análisis y modelado en Python.
La plataforma está construida utilizando Dash, integrando componentes interactivos, gráficos dinámicos y un modelo de clasificación basado en machine learning encargado de asignar un nivel de riesgo a cada ruta operativa.

Justificación de las Tecnologías Utilizadas
Dash

Framework principal seleccionado para la construcción del dashboard:

“Dash es el framework principal utilizado para poder crear el dashboard web interactivo con Python.”

“Se escogió Dash debido a que este fue el más visto en clase, además de que es más intuitivo que Streamlit.”

dash.html

Permite crear elementos HTML para estructurar el layout.

Plotly

“Lo usamos para crear gráficos interactivos y lo escogimos debido a su simplicidad.”

Pandas

“Para la manipulación de DataFrames.”

NumPy

“Para poder manipular arrays y matrices procedentes de los DataFrames.”

scikit-learn – KMeans

“Se utilizó como herramienta de agrupamiento para clasificar los datos de rutas en clústeres.”

scikit-learn – StandardScaler

“Se utilizó para estandarizar los datos antes de aplicar K-Means.”

Requisitos de Instalación

pip install dash
pip install dash-bootstrap-components
pip install dash-auth
pip install plotly
pip install pandas
pip install numpy
pip install scikit-learn

Ejecución de la Aplicación

ejecutar el archivo principal  en la misma carpeta donde se encuentran los archivos necesarios:

Enero-febrero 2025 Combustible.xlsx

Reporte Listado Viaje Ene-Oct_2025.xlsx

Tablero_PL_2024-09_2025-09_v2.xlsx

Telemetría.xlsx

Ejecutar la aplicación con:
python app.py


Abrir el navegador en:
http://localhost:8050

NOTA

Al iniciar pueden aparecer advertencias debido a que algunas librerías se utilizan en procesos de modelado no convencionales. Sin embargo, la ejecución y los resultados son correctos.

Autenticación

La aplicación requiere autenticación básica.
Para este proyecto se utiliza:

Usuario: admin

Contraseña: 1234


Uso del Dashboard

Acceder a la pantalla inicial de Carga de Datos.

Subir los cuatro archivos de Excel en los módulos correspondientes.

La carga puede tardar algunos segundos. (específicamente para viajes, hay que subir el archivo 2 veces dado a que es un archivo muy pesado para el sistema, sale un error pero al cargar por segunda vez funciona)

Una vez cargados los datos, seleccionar el botón “Ir al Dashboard”.

Dentro del dashboard:

Seleccionar o escribir la ruta que se desea analizar.

Explorar los indicadores de nivel de servicio, riesgo del clúster, costos asociados, kilómetros por periodo y simulaciones de buffer.

DIAGRAMA ILUSTRATIVO DE APLICACIÓN 

USUARIO
  └── Navegador Web (localhost:8050)
        │
        ▼
INTERFAZ DASH
  ├── Carga de Archivos (Upload Components)
  ├── Sidebar (Rutas / Navegación)
  ├── Dash Core Components (Dropdowns, Graphs)
  └── Dash Bootstrap Components (Layout visual)
        │
        ▼
CALLBACK ENGINE (Dash)
  ├── Procesamiento de archivos:
  │     ├── Combustible
  │     ├── Viajes
  │     ├── Telemetría
  │     └── Tablero PL
  ├── Cálculo de KPIs:
  │     ├── CPK
  │     ├── Ociosidad Global
  │     └── Ociosidad por Ruta
  ├── Modelo IA:
  │     ├── Limpieza de datos
  │     ├── Feature Engineering
  │     ├── StandardScaler
  │     └── K-Means (Clasificación riesgo)
  └── Simulaciones:
        ├── Trade-off buffer vs NS
        ├── KM por periodo
        └── Costo de buffer por ruta
        │
        ▼
PLOTLY GRAPH ENGINE
  ├── Barras (CPK, KM)
  ├── Líneas (Tradeoff)
  ├── Burbujas y elementos dinámicos
  └── Estilos personalizados (colores corporativos)
        │
        ▼
PÁGINA RENDERIZADA AL USUARIO
