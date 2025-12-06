DASHBOARD LOGIMAYAB POR QUIPO Pi-Thon's

Integrantes del equipo : 
Iker Villalobos Gilling  | A01710453
Juan Carlos Cárcamo Alarcón  | A01710253
José David Castillo Jasso    | A01710953
Ana Isabel García Mojica    | A01706241

LINK a presentación Final 
https://www.canva.com/design/DAG6eULcP2Q/_UzpQETJNqceFTnYF44EUg/edit?utm_content=DAG6eULcP2Q&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

Justificación de las tecnologías usadas

Dash
“Dash es el framework principal utilizado para poder crear el dashboard web interactivo con Python.”
“Se escogió Dash debido a que este fue el más visto en clase, además de que es más intuitivo que Streamlit.”
dash.html
“Permite crear elementos HTML para estructurar el layout.”
plotly
“Lo usamos para crear gráficos interactivos y lo escogimos debido a su simplicidad.”
pandas
“Para la manipulación de DataFrames.”
numpy
“Para poder manipular arrays y matrices procedentes de los DataFrames.”
sklearn.cluster.KMeans
“Se utilizó como herramienta de agrupamiento para clasificar los datos de rutas en clústeres.”
sklearn.preprocessing.StandardScaler
“Se utilizó para estandarizar los datos antes de aplicar K-Means.”

INSTRUCCIONES PARA USO 
pip install Dash
pip install streamlit
import dash
import dash_auth
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import base64
import io
import flask
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler