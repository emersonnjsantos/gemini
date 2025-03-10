from decouple import config
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from langchain.prompts import PromptTemplate

# Carregando o arquivo de estilo externo (style.css)
st.markdown('<link rel="stylesheet" href="style.css">', unsafe_allow_html=True)

# Definindo o template de prompt para viagens
prompt_viagem = PromptTemplate(
    input_variables=["destino", "dica", "idioma"],
    template=""" 
    Você é um assistente de viagens. Seu trabalho é fornecer informações detalhadas sobre destinos turísticos.
    Responda às perguntas com base nas informações mais relevantes e atualizadas sobre o local.
    
    Caso o destino seja fictício ou inexistente, responda: "Não sei".

    Pergunta: Qual é a melhor época para visitar {destino}?
    Responda em {dica} parágrafo(s) no idioma {idioma}.
    
    Dicas para {destino}:
    - Clima
    - Transporte
    - Atrações turísticas
    -restaurantes
    -hotéis
    -preços
    -dicas de segurança
    -dicas de cultura
    -dicas de comportamento
    -dicas de costume
    -dicas de tradição
    """,
)

# Carregando a chave da API do Google Gemini
GOOGLE_GEMINI_KEY = config("GOOGLE_GEMINI_KEY")

# Configurando o modelo com a chave da API
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_GEMINI_KEY)

# Título da aplicação Streamlit
st.title("Meu Agente Guia Turistico IA")

# Coletando entradas do usuário
destino = st.text_input("Digite o nome do destino turístico")
dica = st.number_input("Digite o número de parágrafos", min_value=1, max_value=50)
idioma = st.text_input("Digite o idioma para a resposta")

# Verificando se todas as entradas foram fornecidas
if destino and dica and idioma:
    # Formatando o prompt com os dados fornecidos
    prompt_formatado = prompt_viagem.format(destino=destino, dica=dica, idioma=idioma)
    
    # Invocando o modelo com o prompt formatado
    response = llm.invoke(prompt_formatado)
    
    # Exibindo a resposta gerada pelo modelo
    st.write(response.content)
    
    # Link para abrir o local no Google Maps
    maps_url = f"https://www.google.com/maps/search/?q={destino}"
    st.markdown(f"[Abrir {destino} no Google Maps]({maps_url})", unsafe_allow_html=True)
