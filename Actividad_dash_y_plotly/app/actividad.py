import os
import pandas as pd

# ... otros imports ...

# Construir la ruta absoluta al archivo csv basándose en la ubicación de este script
current_folder = os.path.dirname(__file__)
csv_path = os.path.join(current_folder, 'Market_Trend_External.csv')

df = pd.read_csv(r"/Users/ikvigier/Library/CloudStorage/OneDrive-InstitutoTecnologicoydeEstudiosSuperioresdeMonterrey/TEC/7 Semestre/GitHub/Laboratorio_AnaIsabel/Laboratorio_AnaIsabel/Actividad_dash_y_plotly/app/Market_Trend_External.csv")
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px

# 1. Carga de Datos
# Asegúrate de que 'Market_Trend_External.csv' esté en la misma carpeta que este script.
try:
    df = pd.read_csv("Market_Trend_External.csv")
    # Convertir la columna Date a formato fecha si existe, para mejores gráficas de tiempo
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
except FileNotFoundError:
    print("Error: Archivo 'Market_Trend_External.csv' no encontrado.")
    # Creamos un DataFrame vacío para evitar que la app crashee al iniciar sin datos
    df = pd.DataFrame()

# Paleta de colores del notebook
principales = ["#14283B", "#EED2A8", "#3C8990", "#409FA4", "#3B939C", "#285C6C"]

# 2. Configuración de las 10 Gráficas
# Diccionario que contiene: Título, Función para generar la figura y Descripción Markdown.
graphs_config = {
    'g1': {
        'label': '1. Volatilidad vs. Retorno',
        'title': 'Volatilidad vs. Retorno Diario',
        'desc': """
### Análisis de Volatilidad
Esta gráfica muestra la dispersión de los retornos en función del rango de volatilidad diario.
* **Interpretación:** La mayor concentración de datos suele estar en rangos de volatilidad baja. A medida que la volatilidad (eje X) aumenta, los retornos (eje Y) tienden a dispersarse más, lo que indica que **la alta volatilidad conlleva un mayor riesgo e incertidumbre** (posibilidad de grandes ganancias o grandes pérdidas).
        """,
        'func': lambda d: px.scatter(d, x="Volatility_Range", y="Daily_Return_Pct", color="Volatility_Range",
                                     color_continuous_scale=principales, marginal_y="rug", marginal_x="histogram")
    },
    'g2': {
        'label': '2. Volumen vs. Retorno',
        'title': 'Volumen vs. Retorno Diario',
        'desc': """
### Análisis de Volumen
Visualiza si el volumen de operaciones influye en la magnitud del retorno diario.
* **Interpretación:** Se busca observar si los días con volumen excepcionalmente alto (picos en el eje X) se correlacionan con movimientos drásticos en el precio. Generalmente, el volumen confirma la fuerza de una tendencia.
        """,
        'func': lambda d: px.scatter(d, x="Volume", y="Daily_Return_Pct", color="Volume",
                                     color_continuous_scale=principales)
    },
    'g3': {
        'label': '3. VIX (Índice de Miedo) vs. Retorno',
        'title': 'VIX vs. Retorno Diario',
        'desc': """
### VIX: El Índice del Miedo
El VIX mide la expectativa de volatilidad del mercado a 30 días.
* **Interpretación:** Existe una relación inversa clásica: cuando el VIX sube (más miedo), los mercados tienden a caer o mostrar retornos negativos. Esta gráfica permite validar esa correlación en tus datos.
        """,
        'func': lambda d: px.scatter(d, x="VIX_Close", y="Daily_Return_Pct", color="VIX_Close",
                                     color_continuous_scale=principales)
    },
    'g4': {
        'label': '4. Sentimiento vs. Retorno',
        'title': 'Score de Sentimiento vs. Retorno Diario',
        'desc': """
### Impacto del Sentimiento
Relaciona el sentimiento agregado (noticias, redes sociales) con el desempeño del mercado.
* **Interpretación:** Un puntaje de sentimiento positivo (cercano a 1) debería teóricamente coincidir con retornos positivos. Sin embargo, el mercado a veces reacciona de forma contraria ("comprar el rumor, vender la noticia").
        """,
        'func': lambda d: px.scatter(d, x="Sentiment_Score", y="Daily_Return_Pct", color="Sentiment_Score",
                                     color_continuous_scale=principales)
    },
    'g5': {
        'label': '5. Riesgo Geopolítico vs. Retorno',
        'title': 'Riesgo Geopolítico vs. Retorno Diario',
        'desc': """
### Riesgo Geopolítico
Muestra la sensibilidad del mercado ante eventos globales y tensiones geopolíticas.
* **Interpretación:** Observa si los días con alto score de riesgo geopolítico coinciden consistentemente con retornos negativos, o si el mercado se mantiene resiliente ante estos factores externos.
        """,
        'func': lambda d: px.scatter(d, x="GeoPolitical_Risk_Score", y="Daily_Return_Pct", color="GeoPolitical_Risk_Score",
                                     color_continuous_scale=principales)
    },
    'g6': {
        'label': '6. Índice de Divisa vs. Retorno',
        'title': 'Índice de Moneda vs. Retorno Diario',
        'desc': """
### Fortaleza de la Moneda
Relación entre el índice de la divisa (ej. Dólar) y los retornos del mercado accionario.
* **Interpretación:** Una moneda local muy fuerte puede encarecer las exportaciones, afectando negativamente a empresas multinacionales y, por ende, a los índices bursátiles.
        """,
        'func': lambda d: px.scatter(d, x="Currency_Index", y="Daily_Return_Pct", color="Currency_Index",
                                     color_continuous_scale=principales)
    },
    'g7': {
        'label': '7. Noticias Económicas (Boxplot)',
        'title': 'Distribución de Retornos: Noticias vs. No Noticias',
        'desc': """
### Impacto de Noticias Económicas
Diagrama de caja que compara la distribución de los retornos en días con noticias económicas (1) frente a días sin ellas (0).
* **Interpretación:** Si la caja del grupo '1' es más amplia que la del '0', indica que las noticias económicas introducen mayor volatilidad y dispersión en los resultados del mercado.
        """,
        'func': lambda d: px.box(d, x="Economic_News_Flag", y="Daily_Return_Pct", color="Economic_News_Flag",
                                 color_discrete_sequence=principales)
    },
    'g8': {
        'label': '8. Cambio Tasas Fed (Boxplot)',
        'title': 'Impacto Cambio Tasas Fed en el Retorno',
        'desc': """
### Tasas de Interés Federales
Compara el comportamiento del mercado en días donde la Reserva Federal anunció cambios en las tasas.
* **Interpretación:** Los anuncios de tasas son eventos críticos. Un rango intercuartílico (caja) más grande en el grupo '1' sugiere que estos días son de alta incertidumbre y reajuste de precios.
        """,
        'func': lambda d: px.box(d, x="Federal_Rate_Change_Flag", y="Daily_Return_Pct", color="Federal_Rate_Change_Flag",
                                 color_discrete_sequence=principales)
    },
    'g9': {
        'label': '9. Histórico de Precios',
        'title': 'Evolución del Precio de Cierre',
        'desc': """
### Tendencia de Precios
Gráfico de línea temporal que muestra la evolución del precio de cierre a lo largo del tiempo.
* **Interpretación:** Fundamental para identificar la tendencia general del mercado (alcista, bajista o lateral) y visualizar los ciclos económicos de largo plazo mencionados en el análisis.
        """,
        'func': lambda d: px.line(d, x="Date", y="Close_Price",
                                  color_discrete_sequence=[principales[0]])
    },
    'g10': {
        'label': '10. Distribución de Retornos',
        'title': 'Histograma de Retornos Diarios',
        'desc': """
### Frecuencia de Retornos
Histograma que muestra cómo se distribuyen los porcentajes de retorno diario.
* **Interpretación:** Permite evaluar la normalidad de los datos. Una campana de Gauss perfecta es rara; los mercados suelen tener "colas gordas" (eventos extremos más frecuentes de lo que predice la estadística normal).
        """,
        'func': lambda d: px.histogram(d, x="Daily_Return_Pct", nbins=50,
                                       color_discrete_sequence=[principales[2]])
    }
}

# 3. Inicialización de la App
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# 4. Diseño del Layout
app.layout = dbc.Container([
    # Encabezado
    dbc.Row(
        dbc.Col(html.H1("Dashboard de Análisis de Mercado", className="text-center my-4 text-primary"), width=12)
    ),

    # Dropdown de Selección (Input)
    dbc.Row(
        dbc.Col([
            html.Label("Selecciona un gráfico para visualizar:", className="fw-bold"),
            dcc.Dropdown(
                id='chart-selector',
                options=[{'label': val['label'], 'value': key} for key, val in graphs_config.items()],
                value='g1',  # Valor inicial por defecto
                clearable=False,
                className="mb-4"
            )
        ], width=8, className="mx-auto")
    ),

    # Título de la Gráfica (Output 1)
    dbc.Row(
        dbc.Col(html.H3(id='chart-title', className="text-center mb-2"), width=12)
    ),

    # Gráfica Principal (Output 2)
    dbc.Row(
        dbc.Col(dcc.Graph(id='main-chart', figure={}), width=12)
    ),

    # Descripción en Markdown (Output 3)
    dbc.Row(
        dbc.Col([
            html.H5("Descripción e Interpretación:", className="mt-4"),
            dcc.Markdown(id='chart-description', className="p-3 border rounded bg-light")
        ], width=10, className="mx-auto mb-5")
    )
], fluid=True)

# 5. Callback para interactividad
@app.callback(
    [Output('main-chart', 'figure'),
     Output('chart-title', 'children'),
     Output('chart-description', 'children')],
    [Input('chart-selector', 'value')]
)
def update_dashboard(selected_key):
    # Recuperamos la configuración basada en la selección (fallback a 'g1' si hay error)
    config = graphs_config.get(selected_key, graphs_config['g1'])
    
    # 1. Generamos la figura ejecutando la función guardada en el diccionario
    if not df.empty:
        fig = config['func'](df)
        # Unificamos el estilo de todas las gráficas
        fig.update_layout(template="plotly_white", margin=dict(l=40, r=40, t=40, b=40))
    else:
        fig = {} # Figura vacía si no hay datos

    # 2. Obtenemos el título
    title = config['title']
    
    # 3. Obtenemos la descripción
    desc = config['desc']
    
    return fig, title, desc

# 6. Ejecución del Servidor
if __name__ == '__main__':
    app.run(debug=True, port=8051)