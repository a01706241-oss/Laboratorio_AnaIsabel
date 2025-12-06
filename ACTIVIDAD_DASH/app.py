import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# CARGAR DE DATOS
try:
    df = pd.read_csv("Market_Trend_External.csv")
except FileNotFoundError:
    print("AVISO: No se encontró 'Market_Trend_External.csv'. Asegúrate de que esté en la carpeta.")
    df = pd.DataFrame() 

# PALETAS DE COLORES
principales = ["#14283B", "#EED2A8", "#3C8990", "#409FA4", "#3B939C"]
complementarios = ["#14283B", "#3b2714"]
triada = ["#14283b", "#3b1428", "#283b14"]
complementarios_divididos = ["#14283b", "#2f143b", "#383b14"]

# INICIALIZAR APP
app = dash.Dash(__name__)
server = app.server

# LAYOUT
app.layout = html.Div([
    # ENCABEZADO
    html.Div([
        html.H1("Dashboard Financiero: Market Trends", style={'color': '#14283B', 'fontFamily': 'Arial'}),
        html.H3("Equipo: Iker Villalobos, Juan Carlos Cárcamo, José David Castillo, Ana Isabel García", 
                style={'color': 'gray', 'fontSize': '16px', 'fontFamily': 'Arial'}),
    ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#f4f4f4'}),
    
    html.Hr(),

    # Contenedor Principal
    html.Div([
        # SECCIÓN DE CONTROLES
        html.Div([
            html.Label("Selecciona el gráfico a visualizar:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='selector-grafico',
                options=[
                    {'label': '1. Volatilidad vs. Retorno (Heterocedasticidad)', 'value': 'g1'},
                    {'label': '2. Volumen vs. Retorno (Liquidez)', 'value': 'g2'},
                    {'label': '3. VIX vs. Retorno (Miedo)', 'value': 'g3'},
                    {'label': '4. Evolución Histórica de Precios (OHLC)', 'value': 'g4'},
                    {'label': '5. High vs. Low (Correlación Estructural)', 'value': 'g5'},
                    {'label': '6. Riesgo Geopolítico vs. Retorno', 'value': 'g6'},
                    {'label': '7. Riesgo Geopolítico vs. Volumen', 'value': 'g7'},
                    {'label': '8. Tipo de Cambio vs. Volumen', 'value': 'g8'},
                    {'label': '9. Sentiment Score vs. Retorno', 'value': 'g9'},
                    {'label': '10. Precio Máximo vs. Volumen', 'value': 'g10'},
                    {'label': 'Extra: Evolución Histórica (Time Series)', 'value': 'time_series'}
                ],
                value='g1', 
                clearable=False,
                style={'width': '100%'}
            ),
            html.Div(id='metricas-clave', style={'marginTop': '30px'})
        ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),

        # SECCIÓN DE GRÁFICA 
        html.Div([
            dcc.Graph(id='grafico-output', style={'height': '600px'}),
        ], style={'width': '70%', 'display': 'inline-block', 'padding': '10px'}),
    ]),

    # SECCIÓN DE DESCRIPCIÓN
    html.Div([
        html.H4("Interpretación del Analista:", style={'color': '#14283B'}),
        dcc.Markdown(id='descripcion-output')
    ], style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#e8eff5', 'borderRadius': '10px'})
])

# CALLBACKS
@app.callback(
    [Output('grafico-output', 'figure'),
     Output('descripcion-output', 'children')],
    [Input('selector-grafico', 'value')]
)
def actualizar_dashboard(seleccion):
    
    # G1: Volatilidad vs Retorno
    if seleccion == 'g1':
        fig = px.scatter(df, x="Volatility_Range", y="Daily_Return_Pct", 
                         color="Volatility_Range", title="Volatilidad vs. Retorno Diario",
                         color_continuous_scale=principales,
                         marginal_y="rug", marginal_x="histogram", 
                         hover_data=['Date', 'Close_Price'])
        desc = """
        **Análisis de Heterocedasticidad:**
        Se observa que cuando la volatilidad es baja (0-2), los retornos son estables. A medida que aumenta, la dispersión crece drásticamente.
        Los días con ganancias o pérdidas extremas son "outliers" que solo ocurren en momentos de alta inestabilidad[cite: 132].
        """

    # G2: Volumen vs Retorno
    elif seleccion == 'g2':
        fig = px.scatter(df, x="Volume", y="Daily_Return_Pct", 
                         color="Volume", title="Volumen vs. Retorno Diario",
                         color_continuous_scale=principales,
                         marginal_x="box") 
        desc = """
        **Análisis de Liquidez:**
        Curiosamente, los retornos más extremos (superiores al 200%) tienden a ocurrir en días con volúmenes relativamente menores (0M - 5M)[cite: 169].
        Esto sugiere que el precio es más volátil cuando hay menos liquidez.
        """

    # G3: VIX vs Retorno
    elif seleccion == 'g3':
        fig = px.scatter(df, x="VIX_Close", y="Daily_Return_Pct", 
                         color="VIX_Close", title="VIX (Miedo) vs. Retorno Diario",
                         color_continuous_scale=triada)
        desc = """
        **Impacto del Miedo (VIX):**
        La gráfica confirma que a mayor incertidumbre (VIX alto), mayor es la volatilidad de los rendimientos.
        El miedo no determina la dirección del precio, pero sí magnifica el movimiento[cite: 206].
        """

    # G4: Evolución Histórica
    elif seleccion == 'g4':
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Close_Price'], mode='lines', name='Close', line=dict(color=principales[0])))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['High_Price'], mode='lines', name='High', line=dict(color=principales[1], width=1)))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Low_Price'], mode='lines', name='Low', line=dict(color=principales[2], width=1)))
        
        fig.update_layout(title="Evolución Histórica de Precios (OHLC)", 
                          xaxis_title="Fecha", yaxis_title="Precio",
                          xaxis_rangeslider_visible=True) 
        desc = """
        **Tendencia de Largo Plazo:**
        Visualización de los ciclos económicos (alcistas y bajistas) a lo largo de la historia.
        Usa el deslizador inferior para hacer zoom en periodos específicos[cite: 100].
        """

    # G5: High vs Low
    elif seleccion == 'g5':
        fig = px.scatter(df, x="Low_Price", y="High_Price", 
                         color="High_Price", title="High vs. Low (Spread Intradía)",
                         color_continuous_scale=complementarios_divididos)
        desc = """
        **Correlación Estructural:**
        Correlación positiva extremadamente fuerte. El precio máximo rara vez se desvía drásticamente del mínimo, indicando estabilidad intradía consistente[cite: 271].
        """

    # G6: Riesgo Geo vs Retorno
    elif seleccion == 'g6':
        fig = px.scatter(df, x="GeoPolitical_Risk_Score", y="Daily_Return_Pct",
                         color="GeoPolitical_Risk_Score", title="Riesgo Geopolítico vs. Retorno",
                         color_continuous_scale=principales)
        desc = """
        **Independencia del Riesgo:**
        La distribución horizontal indica que el retorno diario no depende linealmente del riesgo geopolítico.
        El mercado genera retornos extremos tanto en paz como en tensión global[cite: 308].
        """

    # G7: Riesgo Geo vs Volumen
    elif seleccion == 'g7':
        fig = px.scatter(df, x="GeoPolitical_Risk_Score", y="Volume",
                         color="Volume", title="Riesgo Geopolítico vs. Volumen",
                         color_continuous_scale=complementarios_divididos)
        desc = """
        **Resiliencia del Volumen:**
        La distribución rectangular muestra que el volumen de negociación se mantiene constante sin importar el nivel de riesgo geopolítico[cite: 341].
        """

    # G8: Currency vs Volumen
    elif seleccion == 'g8':
        fig = px.scatter(df, x="Currency_Index", y="Volume",
                         color="Volume", title="Tipo de Cambio vs. Volumen",
                         color_continuous_scale=["#000000", "#0a1016", "#111a24"]) 
        desc = """
        **Estabilidad Cambiaria:**
        Al igual que con el riesgo político, el volumen operado no parece verse afectado drásticamente por el nivel del tipo de cambio[cite: 376].
        """

    # G9: Sentiment vs Retorno
    elif seleccion == 'g9':
        fig = px.scatter(df, x="Sentiment_Score", y="Daily_Return_Pct",
                         color="Sentiment_Score", title="Sentiment Score vs. Retorno",
                         color_continuous_scale=principales)
        desc = """
        **Sentimiento de Mercado:**
        La dispersión horizontal sugiere que el sentimiento público (noticias/redes) no es un predictor lineal inmediato del precio.
        Días con sentimiento muy positivo pueden tener retornos negativos y viceversa[cite: 412].
        """
        
    # G10: High vs Volumen 
    elif seleccion == 'g10':
        fig = px.scatter(df, x="High_Price", y="Volume",
                         color="High_Price", title="Precio Máximo del Día vs. Volumen",
                         color_continuous_scale=triada)
        desc = """
        **Análisis de Precio vs Volumen:**
        Esta gráfica permite ver si los precios más altos atraen más volumen. 
        Generalmente, se busca ver si hay "euforia" (mucho volumen en precios máximos).
        """

    # Extra: Time Series (La de Matplotlib convertida a Plotly)
    elif seleccion == 'time_series':
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Close_Price'], mode='lines', name='Close', line=dict(color=principales[0])))
        fig.update_layout(title="Evolución Histórica de Precios", xaxis_rangeslider_visible=True)
        desc = "Análisis: Evolución histórica de precios con selector de rango temporal."
    else:
        fig = px.scatter(title="Selecciona un gráfico")
        desc = "Selecciona una opción del menú."

    return fig, desc

if __name__ == '__main__':
    app.run(debug=True, port=8051)