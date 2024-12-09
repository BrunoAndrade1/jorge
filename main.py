import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
import io

# Configuração da página
st.set_page_config(page_title="Dashboard ESG, Emissões e Bonds", layout="wide")

# Funções para download de arquivos
def get_table_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def get_table_download_link_excel(df, filename, text):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Dados')
    writer.close()
    processed_data = output.getvalue()
    b64 = base64.b64encode(processed_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Título e Introdução
st.title("Dashboard de Avaliação de Empresas - ESG, Emissões e Bonds")
st.markdown("""
Este dashboard permite visualizar e analisar indicadores ESG, emissões de CO2, indicadores de títulos de dívida (bonds) e status de conformidade das empresas. Você pode carregar seus próprios dados ou usar os dados de exemplo fornecidos.
""")

# Opção para carregar dados
st.sidebar.header("📂 Carregar Dados")
upload_file = st.sidebar.file_uploader("Faça upload do seu arquivo Excel ou CSV", type=['xlsx', 'csv'])

if upload_file is not None:
    try:
        if upload_file.name.endswith('.csv'):
            df = pd.read_csv(upload_file)
        else:
            df = pd.read_excel(upload_file)
        st.success("Dados carregados com sucesso!")
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        st.stop()
else:
    st.info("Dados Carregandos...")
    # Dados de exemplo expandidos com mais empresas e indicadores
    data = {
        'CNPJ': [
            '12.345.678/0001-90', '98.765.432/0001-10', '11.111.111/0001-99',
            '22.222.222/0001-88', '33.333.333/0001-77', '44.444.444/0001-66',
            '55.555.555/0001-55', '66.666.666/0001-44', '77.777.777/0001-33',
            '88.888.888/0001-22'
        ],
        'Empresa': [
            'TechNova', 'EcoEnergia', 'Construtora Silva', 'InovaTech',
            'AgroVerde', 'Finanças Prime', 'SaúdePlus', 'TransPortes',
            'VarejoMax', 'EducaMais'
        ],
        'Setor': [
            'Tecnologia', 'Energia Renovável', 'Construção', 'Tecnologia',
            'Agricultura', 'Serviços Financeiros', 'Saúde', 'Transporte',
            'Varejo', 'Educação'
        ],
        'Valor_emprestimo': [
            1000000, 500000, 300000, 800000, 600000,
            700000, 400000, 900000, 750000, 650000
        ],
        # Indicadores Ambientais (Green Bonds)
        'Emissoes_CO2': [820000, 10000, 150000, 80000, 300000, 200000, 120000, 500000, 250000, 180000],
        'Energia_Renovavel_Pcnt': [30, 95, 45, 60, 25, 50, 40, 55, 35, 65],
        'Reducao_Residuos_Ton': [150, 80, 45, 95, 60, 70, 50, 85, 55, 65],
        'Economia_Agua_M3': [5000, 3000, 2000, 4000, 3500, 4500, 2500, 4800, 3200, 4100],
        'Meta_Carbono_Neutro': [2030, 2025, 2035, 2028, 2040, 2032, 2033, 2027, 2031, 2029],
        'Certificacoes_Ambientais': [3, 5, 2, 4, 1, 3, 2, 4, 2, 5],
        # Indicadores Sociais (Social Bonds)
        'Empregos_Criados': [50, 100, 30, 60, 45, 55, 35, 65, 58, 62],
        'Empregos_Vulneraveis': [15, 30, 8, 20, 12, 18, 10, 22, 16, 19],
        'Beneficiarios_Projetos': [1000, 2000, 500, 1500, 800, 1200, 600, 1600, 900, 1100],
        'Investimento_Social_K': [500, 800, 300, 600, 400, 550, 350, 650, 450, 500],
        'Diversidade_Genero_Pcnt': [45, 55, 35, 50, 40, 48, 42, 51, 39, 47],
        'Projetos_Comunidade': [5, 8, 3, 6, 4, 5, 4, 7, 5, 6],
        # Pontuações ESG
        'ESG_Score': [75, 85, 65, 90, 70, 78, 72, 88, 80, 82],
        'E_Score': [70, 90, 60, 95, 65, 80, 75, 85, 70, 83],
        'S_Score': [80, 80, 70, 85, 75, 76, 74, 90, 78, 80],
        'G_Score': [75, 85, 65, 88, 70, 78, 68, 89, 76, 83],
        # Indicadores de Governança
        'Transparencia_Score': [85, 90, 75, 88, 80, 82, 78, 91, 84, 86],
        'Politicas_ESG': [True, True, False, True, True, True, False, True, True, True],
        'Comite_Sustentabilidade': [True, True, False, True, False, True, False, True, True, True],
        'Reportes_GRI': [True, True, False, True, False, True, False, True, True, True],
        # Indicadores de Bonds
        'Credit_Rating': ['A', 'BBB', 'AA', 'CCC', 'A', 'BBB', 'AA', 'CCC', 'A', 'BBB'],
        'YTM': [5.0, 4.5, 6.0, 7.5, 5.5, 4.8, 6.2, 7.8, 5.3, 4.7],
        'Duration': [5, 7, 3, 10, 6, 8, 4, 11, 5, 7],
        'Total_Bonds_Issued': [500000, 750000, 300000, 450000, 600000, 800000, 350000, 900000, 400000, 700000],
        'Fator_emissao': [0.82, 0.02, 0.5, 0.1, 0.3, 0.25, 0.4, 0.35, 0.28, 0.22]
    }
    df = pd.DataFrame(data)

# Verificação de colunas necessárias
required_columns = [
    'CNPJ', 'Empresa', 'Setor', 'Valor_emprestimo', 'Fator_emissao',
    'Empregos_Criados', 'ESG_Score', 'E_Score', 'S_Score', 'G_Score',
    'Credit_Rating', 'YTM', 'Duration', 'Total_Bonds_Issued',
    'Energia_Renovavel_Pcnt', 'Emissoes_CO2', 'Reducao_Residuos_Ton',
    'Economia_Agua_M3', 'Meta_Carbono_Neutro', 'Certificacoes_Ambientais',
    'Empregos_Vulneraveis', 'Beneficiarios_Projetos', 'Investimento_Social_K',
    'Diversidade_Genero_Pcnt', 'Projetos_Comunidade',
    'Transparencia_Score', 'Politicas_ESG',
    'Comite_Sustentabilidade', 'Reportes_GRI'
]
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    st.error(f"Faltando colunas no DataFrame: {', '.join(missing_columns)}")
    st.stop()

# Processamento dos dados
df['Emissoes_CO2'] = df['Valor_emprestimo'] * df['Fator_emissao']  # Em kgCO2
df['Intensidade_carbono'] = df['Emissoes_CO2'] / df['Valor_emprestimo']
df['Impacto_Social_Score'] = (df['Empregos_Criados'] + df['Beneficiarios_Projetos']/100) / 2

# Avaliação de conformidade
green_bond_threshold = {
    'Energia_Renovavel_Pcnt': 40,
    'Emissoes_CO2': 500000,
    'Certificacoes_Ambientais': 2
}
social_bond_threshold = {
    'Empregos_Criados': 40,
    'Empregos_Vulneraveis': 10,
    'Investimento_Social_K': 400
}

def avaliar_conformidade(row):
    green_conformity = (
        row['Energia_Renovavel_Pcnt'] >= green_bond_threshold['Energia_Renovavel_Pcnt'] and
        row['Emissoes_CO2'] <= green_bond_threshold['Emissoes_CO2'] and
        row['Certificacoes_Ambientais'] >= green_bond_threshold['Certificacoes_Ambientais']
    )
    social_conformity = (
        row['Empregos_Criados'] >= social_bond_threshold['Empregos_Criados'] and
        row['Empregos_Vulneraveis'] >= social_bond_threshold['Empregos_Vulneraveis'] and
        row['Investimento_Social_K'] >= social_bond_threshold['Investimento_Social_K']
    )
    if green_conformity and social_conformity:
        return 'Totalmente Conforme'
    elif green_conformity:
        return 'Conforme Green Bond'
    elif social_conformity:
        return 'Conforme Social Bond'
    else:
        return 'Não Conforme'

df['Status_Conformidade'] = df.apply(avaliar_conformidade, axis=1)

# Cálculo de Risco ESG
def calcular_risco_esg(row):
    risco_ambiental = (100 - row['E_Score']) * (row['Emissoes_CO2'] / 1000000)
    risco_social = (100 - row['S_Score']) * (1 - row['Empregos_Vulneraveis']/row['Empregos_Criados'])
    risco_governanca = (100 - row['G_Score']) * (1 if not row['Comite_Sustentabilidade'] else 0.5)
    risco_total = (risco_ambiental + risco_social + risco_governanca) / 3
    if risco_total < 30:
        return 'Baixo'
    elif risco_total < 60:
        return 'Médio'
    else:
        return 'Alto'

df['Risco_ESG'] = df.apply(calcular_risco_esg, axis=1)

# Cálculo de médias do setor para benchmarking
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

# Certifique-se de NÃO excluir 'Emissoes_CO2' se você precisar usá-la posteriormente
cols_to_exclude = ['Valor_emprestimo', 'Total_Bonds_Issued']  # Removido 'Emissoes_CO2'

numeric_cols = [col for col in numeric_cols if col not in cols_to_exclude]

# Agrupar por setor e calcular a média
setor_media = df.groupby('Setor')[numeric_cols].mean().reset_index()

# Verificação adicional para garantir que 'Emissoes_CO2' está presente
if 'Emissoes_CO2' not in setor_media.columns:
    st.error("A coluna 'Emissoes_CO2' não está presente no DataFrame de médias por setor.")
    st.stop()

# Cálculo de risco baseado em Credit Rating
def calcular_risco(row):
    if row['Credit_Rating'] in ['CCC', 'B', 'BB']:
        return 'Alto Risco'
    elif row['Credit_Rating'] in ['A', 'BBB', 'AA']:
        return 'Baixo Risco'
    else:
        return 'Médio Risco'

df['Risk_Level'] = df.apply(calcular_risco, axis=1)

# Filtros Interativos
st.sidebar.header("🔍 Filtros")
setores = st.sidebar.multiselect("Selecione os Setores", options=df['Setor'].unique(), default=df['Setor'].unique())
status_conformidade = st.sidebar.multiselect("Status de Conformidade", options=df['Status_Conformidade'].unique(), default=df['Status_Conformidade'].unique())
esg_score_min = st.sidebar.slider("Pontuação ESG Mínima", min_value=0, max_value=100, value=int(df['ESG_Score'].min()))
esg_score_max = st.sidebar.slider("Pontuação ESG Máxima", min_value=0, max_value=100, value=int(df['ESG_Score'].max()))
credit_ratings = st.sidebar.multiselect("Selecione os Ratings de Crédito", options=df['Credit_Rating'].unique(), default=df['Credit_Rating'].unique())
ytm_min = st.sidebar.slider("Yield to Maturity (YTM) Mínimo (%)", min_value=0.0, max_value=20.0, value=0.0)
ytm_max = st.sidebar.slider("Yield to Maturity (YTM) Máximo (%)", min_value=0.0, max_value=20.0, value=20.0)

df_filtered = df[
    (df['Setor'].isin(setores)) &
    (df['Status_Conformidade'].isin(status_conformidade)) &
    (df['ESG_Score'] >= esg_score_min) &
    (df['ESG_Score'] <= esg_score_max) &
    (df['Credit_Rating'].isin(credit_ratings)) &
    (df['YTM'] >= ytm_min) &
    (df['YTM'] <= ytm_max)
]

# Resumo de KPIs
st.header("Resumo dos Indicadores")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    total_empresas = df_filtered['Empresa'].nunique()
    st.metric("Total de Empresas", total_empresas)
with col2:
    media_esg = df_filtered['ESG_Score'].mean()
    st.metric("Média da Pontuação ESG", f"{media_esg:.2f}")
with col3:
    total_emissoes = df_filtered['Emissoes_CO2'].sum()
    st.metric("Total de Emissões de CO2", f"{total_emissoes:,.2f} kg")
with col4:
    empresas_aprovadas = df_filtered[
        df_filtered['Status_Conformidade'].isin([
            'Totalmente Conforme',
            'Conforme Green Bond',
            'Conforme Social Bond'
        ])
    ]['Empresa'].nunique()
    st.metric("Empresas Aprovadas", empresas_aprovadas)
with col5:
    media_ytm = df_filtered['YTM'].mean()
    st.metric("Média do YTM (%)", f"{media_ytm:.2f}%")
    
    
# #####################################################################
# # Debug - Mostrar distribuição dos status
# st.write("Distribuição dos Status de Conformidade:")
# st.write(df_filtered['Status_Conformidade'].value_counts())
# ######################################################################


# Botão para download dos dados filtrados
st.markdown(get_table_download_link(df_filtered, 'dados_filtrados.csv', '📥 Baixar Dados Filtrados'), unsafe_allow_html=True)

# Organização em abas
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Dados das Empresas",
    "📈 Análises Visuais",
    "📉 Benchmarking",
    "📊 Bonds",
    "ℹ️ Sobre os Indicadores",
    "📈 Análises Detalhadas",
    "📊 Análise Comparativa"
])

with tab1:
    st.header("Dados das Empresas")
    st.dataframe(df_filtered[
        ['CNPJ', 'Empresa', 'Setor', 'Valor_emprestimo', 'Emissoes_CO2', 'Intensidade_carbono',
         'ESG_Score', 'E_Score', 'S_Score', 'G_Score', 'Empregos_Criados',
         'Credit_Rating', 'YTM', 'Duration', 'Total_Bonds_Issued', 'Risk_Level', 'Status_Conformidade']
    ])

with tab2:
    st.header("Análises Visuais")
    # Exemplo: Gráfico de Subpontuações ESG com Labels
    st.subheader("Subpontuações ESG por Empresa")
    df_melted = df_filtered.melt(id_vars=['Empresa'], value_vars=['E_Score', 'S_Score', 'G_Score'],
                                 var_name='Categoria', value_name='Pontuação')
    fig_subscores = px.bar(
        df_melted,
        x='Empresa',
        y='Pontuação',
        color='Categoria',
        barmode='group',
        title='Subpontuações ESG por Empresa',
        height=400,
        text='Pontuação'  # Adiciona rótulos
    )
    fig_subscores.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_subscores.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig_subscores, use_container_width=True)
    
    # Adicione outros gráficos conforme necessário

with tab3:
    st.header("Benchmarking por Setor")
    setor_selecionado = st.selectbox("Selecione um Setor para Benchmarking", options=setor_media['Setor'].unique())
    media_setor = setor_media[setor_media['Setor'] == setor_selecionado]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Média ESG Score do Setor", f"{media_setor['ESG_Score'].values[0]:.2f}")
    with col2:
        st.metric("Média Emissões CO2 do Setor", f"{media_setor['Emissoes_CO2'].values[0]:,.2f} kg")
    with col3:
        st.metric("Média Empregos Criados do Setor", f"{media_setor['Empregos_Criados'].values[0]:.2f}")
    with col4:
        st.metric("Média YTM do Setor (%)", f"{media_setor['YTM'].values[0]:.2f}%")
    
    # Comparação com a média do setor
    st.subheader(f"Comparação das Empresas do Setor {setor_selecionado}")
    df_setor = df_filtered[df_filtered['Setor'] == setor_selecionado]
    fig_comparacao = px.bar(
        df_setor.melt(id_vars=['Empresa'], value_vars=['ESG_Score', 'E_Score', 'S_Score', 'G_Score'],
                     var_name='Pontuação', value_name='Valor'),
        x='Empresa',
        y='Valor',
        color='Pontuação',
        barmode='group',
        title=f"Pontuações ESG das Empresas do Setor {setor_selecionado}",
        height=400,
        text='Valor'  # Adiciona rótulos
    )
    fig_comparacao.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_comparacao.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig_comparacao, use_container_width=True)

with tab4:
    st.header("Indicadores de Bonds")
    # Exemplo: Gráfico de Ratings de Crédito com Tooltips Detalhados
    st.subheader("Ratings de Crédito das Empresas")
    fig_rating = px.bar(
        df_filtered,
        x='Empresa',
        y='Credit_Rating',
        color='Credit_Rating',
        title='Ratings de Crédito das Empresas',
        height=400,
        hover_data={
            'Empresa': True,
            'Credit_Rating': True,
            'ESG_Score': True
        }
    )
    st.plotly_chart(fig_rating, use_container_width=True)
    
    # Adicione outros gráficos conforme necessário

with tab5:
    st.header("Sobre os Indicadores")
    st.markdown("""
    **Pontuação ESG**: Avaliação geral da empresa em termos ambientais, sociais e de governança.
    
    **E_Score (Ambiental)**: Reflete o desempenho da empresa em questões ambientais, como emissões de CO2, eficiência energética e gestão de resíduos.
    
    **S_Score (Social)**: Mede o desempenho em aspectos sociais, incluindo condições de trabalho, diversidade e impacto na comunidade.
    
    **G_Score (Governança)**: Avalia a estrutura de governança corporativa, transparência e práticas éticas.
    
    **Emissões de CO2**: Total de emissões de dióxido de carbono associadas ao valor do empréstimo.
    
    **Intensidade de Carbono**: Emissões de CO2 divididas pelo valor do empréstimo, indicando a quantidade de emissões por real financiado.
    
    **Empregos Criados**: Número de empregos gerados pela empresa como resultado do financiamento.
    
    **Credit_Rating**: Classificação de crédito da empresa fornecida por agências reconhecidas (e.g., S&P, Moody's, Fitch).
    
    **Yield to Maturity (YTM)**: Taxa de retorno esperada se o bond for mantido até o vencimento.
    
    **Duration**: Medida de sensibilidade do preço do bond às variações nas taxas de juros.
    
    **Total_Bonds_Issued**: Valor total de bonds emitidos pela empresa.
    
    **Risk_Level**: Nível de risco baseado no Credit Rating:
    
    - **Baixo Risco**: Ratings de crédito como A, BBB, AA.
    - **Médio Risco**: Ratings intermediários.
    - **Alto Risco**: Ratings de crédito como CCC, B, BB.
    
    **Status de Conformidade**: Indica se a empresa está "Totalmente Conforme", "Conforme Green Bond", "Conforme Social Bond" ou "Não Conforme" com base nos critérios definidos (pontuação ESG, empregos criados, etc.).
    """)

with tab6:
    st.header("📈 Análises Detalhadas")
    # Seletor de empresa para análise detalhada
    empresa_selecionada = st.selectbox("Selecione uma empresa para análise detalhada", df_filtered['Empresa'].unique())
    empresa_data = df_filtered[df_filtered['Empresa'] == empresa_selecionada].iloc[0]
    
    # Radar chart com múltiplos indicadores
    categories = ['E_Score', 'S_Score', 'G_Score', 'Transparencia_Score']
    values = [empresa_data[cat] for cat in categories]
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=['Ambiental', 'Social', 'Governança', 'Transparência'],
        fill='toself',
        marker=dict(color='green')
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        title='Análise Multi-dimensional'
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Tabela detalhada
    st.subheader("Detalhamento dos Indicadores")
    detailed_cols = [
        'ESG_Score', 'E_Score', 'S_Score', 'G_Score',
        'Energia_Renovavel_Pcnt', 'Emissoes_CO2',
        'Empregos_Criados', 'Investimento_Social_K',
        'Status_Conformidade'
    ]
    st.dataframe(df_filtered[df_filtered['Empresa'] == empresa_selecionada][detailed_cols])
    
    # Função para gerar relatório da empresa
    def gerar_relatorio_empresa(empresa_data):
        report = f"""Relatório de Análise ESG - {empresa_data['Empresa']}
1. INFORMAÇÕES GERAIS
---------------------
CNPJ: {empresa_data['CNPJ']}
Setor: {empresa_data['Setor']}
Valor do Empréstimo: R$ {empresa_data['Valor_emprestimo']:,.2f}
Status de Conformidade: {empresa_data['Status_Conformidade']}

2. INDICADORES AMBIENTAIS
-------------------------
Emissões CO2: {empresa_data['Emissoes_CO2']:,.2f} kg
Energia Renovável: {empresa_data['Energia_Renovavel_Pcnt']}%
Redução de Resíduos: {empresa_data['Reducao_Residuos_Ton']} ton
Economia de Água: {empresa_data['Economia_Agua_M3']} m³
Meta Carbono Neutro: {empresa_data['Meta_Carbono_Neutro']}
Certificações: {empresa_data['Certificacoes_Ambientais']}

3. INDICADORES SOCIAIS
----------------------
Empregos Criados: {empresa_data['Empregos_Criados']}
Empregos Vulneráveis: {empresa_data['Empregos_Vulneraveis']}
Beneficiários: {empresa_data['Beneficiarios_Projetos']}
Investimento Social: R$ {empresa_data['Investimento_Social_K']*1000:,.2f}
Diversidade de Gênero: {empresa_data['Diversidade_Genero_Pcnt']}%
Projetos na Comunidade: {empresa_data['Projetos_Comunidade']}

4. PONTUAÇÕES ESG
-----------------
ESG Score Total: {empresa_data['ESG_Score']}
Score Ambiental: {empresa_data['E_Score']}
Score Social: {empresa_data['S_Score']}
Score Governança: {empresa_data['G_Score']}

5. GOVERNANÇA
-------------
Transparência: {empresa_data['Transparencia_Score']}
Políticas ESG: {'Sim' if empresa_data['Politicas_ESG'] else 'Não'}
Comitê de Sustentabilidade: {'Sim' if empresa_data['Comite_Sustentabilidade'] else 'Não'}
Relatórios GRI: {'Sim' if empresa_data['Reportes_GRI'] else 'Não'}
"""
        return report

    # Botão para gerar e baixar relatório
    if st.button("Gerar Relatório"):
        relatorio = gerar_relatorio_empresa(empresa_data)
        st.text_area("Relatório Detalhado", relatorio, height=500)
        
        # Botão para download do relatório
        st.download_button(
            label="📥 Baixar Relatório (TXT)",
            data=relatorio,
            file_name=f"relatorio_{empresa_selecionada.replace(' ', '_')}.txt",
            mime="text/plain"
        )

with tab7:
    st.header("📊 Análise Comparativa")
    st.subheader("Comparação de Empresas")
    
    # Seleção de empresas para comparação
    empresas_comparacao = st.multiselect(
        "Selecione até 3 empresas para comparação",
        df_filtered['Empresa'].unique(),
        default=df_filtered['Empresa'].unique()[:3]
    )
    
    if empresas_comparacao:
        df_comparacao = df_filtered[df_filtered['Empresa'].isin(empresas_comparacao)]
        
        # Gráfico de radar comparativo
        fig_radar_comp = go.Figure()
        for empresa in empresas_comparacao:
            empresa_data = df_comparacao[df_comparacao['Empresa'] == empresa].iloc[0]
            fig_radar_comp.add_trace(go.Scatterpolar(
                r=[empresa_data['E_Score'], empresa_data['S_Score'], empresa_data['G_Score'], empresa_data['Transparencia_Score']],
                theta=['Ambiental', 'Social', 'Governança', 'Transparência'],
                fill='toself',
                name=empresa
            ))
        
        fig_radar_comp.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            title='Comparação de Scores ESG'
        )
        
        st.plotly_chart(fig_radar_comp, use_container_width=True)
        
        # Tabela comparativa
        st.subheader("Tabela Comparativa de Scores ESG")
        comparacao_cols = ['Empresa', 'E_Score', 'S_Score', 'G_Score', 'Transparencia_Score']
        st.dataframe(df_comparacao[comparacao_cols])

# Melhorias na Interface do Usuário
st.markdown("""
<style>
    .stButton > button {
        color: white;
        background-color: #4CAF50;
        border-radius: 5px;
        padding: 8px 16px;
        margin-top: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 18px;
    }
    .css-1d391kg {
        margin-top: -50px;
    }
</style>
""", unsafe_allow_html=True)
