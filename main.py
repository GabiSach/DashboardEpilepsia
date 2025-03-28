import streamlit as st
import pandas as pd
import plotly.express as px

# Configurações de design
BACKGROUND_COLOR = "#dad6ca"
TEXT_COLOR = "#283282"
COLOR_BLUE = "#283282"
COLOR_ORANGE = "#ff761b"

# Configuração da página Streamlit com wide mode desativado
st.set_page_config(page_title="Dashboard Epilepsia", page_icon=":bar_chart:", layout="centered")

st.markdown(
    f"""
    <style>
    body {{
        background-color: {BACKGROUND_COLOR};
        color: {TEXT_COLOR};
    }}
    .stPlot {{
        background-color: {BACKGROUND_COLOR};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Caminho do arquivo TSV
tsv_file = r"C:\Users\gabri\OneDrive\Documentos\UNICAMPRegeneraçãoNervosa\EpilepsiaDadosLT\participants.tsv"

# Caminhos das imagens
image_paths = [
    r"C:\Users\gabri\OneDrive\Documentos\UNICAMPRegeneraçãoNervosa\FotosDashboard\1EPILEPSIA.png",
    r"C:\Users\gabri\OneDrive\Documentos\UNICAMPRegeneraçãoNervosa\FotosDashboard\2EPILEPSIA.png",
    r"C:\Users\gabri\OneDrive\Documentos\UNICAMPRegeneraçãoNervosa\FotosDashboard\3EPILEPSIA.png",
    r"C:\Users\gabri\OneDrive\Documentos\UNICAMPRegeneraçãoNervosa\FotosDashboard\4EPILEPSIA.png",
    r"C:\Users\gabri\OneDrive\Documentos\UNICAMPRegeneraçãoNervosa\FotosDashboard\5EPILEPSIA.png",
    r"C:\Users\gabri\OneDrive\Documentos\UNICAMPRegeneraçãoNervosa\FotosDashboard\6EPILEPSIA.png",
    r"C:\Users\gabri\OneDrive\Documentos\UNICAMPRegeneraçãoNervosa\FotosDashboard\7EPILEPSIA.png"
]

# Carregar dados do arquivo TSV
df = pd.read_csv(tsv_file, sep='\t')

# Dicionário de tradução
traducao = {
    'M': 'Masculino',
    'F': 'Feminino',
    'Patient': 'Paciente',
    'Healthy': 'Saudável'
}

# Aplicar tradução
df['Group'] = df['Group'].map(traducao)

# Funções auxiliares
def personalizar_grafico(fig):
    fig.update_layout(
        legend_title_font_size=30,
        legend_font_size=24,
        legend_itemsizing='constant',
        legend_itemwidth=30,
        xaxis_title_font_size=24,
        yaxis_title_font_size=24,
        xaxis_tickfont_size=20,
        yaxis_tickfont_size=20,
        xaxis_title_text=f"<b>{fig.layout.xaxis.title.text}</b>",
        yaxis_title_text=f"<b>{fig.layout.yaxis.title.text}</b>"
    )
    fig.update_traces(textfont_size=30)
    return fig

def titulo_centralizado(texto, tamanho=36):
    return st.markdown(f"<h2 style='text-align: center; font-size: {tamanho}px;'><b>{texto}</b></h2>", unsafe_allow_html=True)

# Imagens
for image_path in image_paths:
    st.image(image_path)

# Total de entrevistados (imagem em vez de texto)
titulo_centralizado("Total de Entrevistados")
st.image(r"C:\Users\gabri\OneDrive\Documentos\UNICAMPRegeneraçãoNervosa\FotosDashboard\9EPILEPSIA.png")

# Gráfico de pizza de pacientes e saudáveis (personalizado)
titulo_centralizado("Distribuição de Pacientes e Saudáveis")
group_counts = df['Group'].value_counts()
group_fig = personalizar_grafico(px.pie(names=group_counts.index, values=group_counts.values, color_discrete_sequence=[COLOR_BLUE, COLOR_ORANGE]))
st.plotly_chart(group_fig)

# Gráfico de pizza de gênero (com rótulos personalizados)
titulo_centralizado("Gênero dos Entrevistados")
gender_labels = {'M': 'Homens', 'F': 'Mulheres'}
gender_fig = personalizar_grafico(px.pie(df, names=df['gender'].map(gender_labels), color_discrete_sequence=[COLOR_BLUE, COLOR_ORANGE]))
gender_fig.update_traces(texttemplate='%{label}: %{value}', textposition='outside')
st.plotly_chart(gender_fig)

# Histograma de idade (com rótulos dos eixos alterados)
titulo_centralizado("Distribuição de Idade")
age_fig = px.histogram(df, x='age', color_discrete_sequence=[COLOR_BLUE])
age_fig.update_layout(
    xaxis_title_text='Idade',
    yaxis_title_text='Quantidade',
)
st.plotly_chart(personalizar_grafico(age_fig))

# Gráfico de barras de tipo de epilepsia (com rótulos dos eixos alterados)
titulo_centralizado("Tipos de Epilepsia")
epilepsy_counts = df[df['Group'] == 'Paciente']['TLEside'].value_counts()
epilepsy_fig = px.bar(x=epilepsy_counts.index, y=epilepsy_counts.values, color_discrete_sequence=[COLOR_ORANGE])
epilepsy_fig.update_layout(
    xaxis_title_text='Tipo',
    yaxis_title_text='Quantidade de pacientes',
)
st.plotly_chart(personalizar_grafico(epilepsy_fig))

# Boxplot de QI (com rótulos dos eixos alterados)
titulo_centralizado("Comparação de QI")
iq_fig = px.box(df, x='Group', y='IQ', color_discrete_sequence=[COLOR_BLUE, COLOR_ORANGE])
iq_fig.update_layout(
    xaxis_title_text='Grupo',
    yaxis_title_text='QI',
)
iq_fig.update_yaxes(range=[df['IQ'].min() - 5, df['IQ'].max() + 5])
st.plotly_chart(iq_fig)

# Imagem adicional
st.image(r"C:\Users\gabri\OneDrive\Documentos\UNICAMPRegeneraçãoNervosa\FotosDashboard\8EPILEPSIA.png")

# Comparação de volume do hipocampo (com rótulo do eixo x alterado)
titulo_centralizado("Comparação de Volume do Hipocampo")
hippocampus_data = df.groupby('Group')[['L.hipp Volume', 'R.hipp Volume']].mean().reset_index()
hippocampus_data['Diferença (%)'] = ((hippocampus_data['R.hipp Volume'] - hippocampus_data['L.hipp Volume']) / hippocampus_data['L.hipp Volume']) * 100
hippocampus_fig = personalizar_grafico(px.bar(hippocampus_data, x='Group', y='Diferença (%)', color_discrete_sequence=[COLOR_ORANGE]))
hippocampus_fig.update_layout(
    xaxis_title_text='Grupo',
)
st.plotly_chart(personalizar_grafico(hippocampus_fig))

# Gráfico de pizza de presença de MTS (com rótulos personalizados)
titulo_centralizado("Presença de MTS em Pacientes")
mts_labels = {0: 'Ausente', 1: 'Presente'}
mts_fig = personalizar_grafico(px.pie(df, names=df['hasMTS'].map(mts_labels), color_discrete_sequence=[COLOR_ORANGE, COLOR_BLUE]))
st.plotly_chart(mts_fig)

# Fonte (imagem em vez de texto)
titulo_centralizado("Fonte")
st.image(r"C:\Users\gabri\OneDrive\Documentos\UNICAMPRegeneraçãoNervosa\FotosDashboard\10EPILEPSIA.png")

# Fonte (imagem em vez de texto)
titulo_centralizado("Muito obrigada! ❤")
