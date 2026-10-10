
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="Painel de Clientes",
    page_icon="📊",
    layout="wide"
)

# Aparência do painel
st.markdown("""
<style>
.stApp {
    background-color: #101010;
    color: white;
}
h1, h2, h3 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Painel de Análise de Clientes")
st.write("Sistema interativo de análise de dados")

# Base de dados fictícia
dados = {
    "Cliente A": [10, 25, 15, 30, 20],
    "Cliente B": [18, 12, 28, 22, 35],
    "Cliente C": [30, 20, 25, 15, 40]
}

meses = ["Jan", "Fev", "Mar", "Abr", "Mai"]

# Selecionar cliente
st.subheader("Seleção de cliente")

cliente = st.selectbox(
    "Escolha um cliente:",
    list(dados.keys())
)

# Criar tabela
tabela = pd.DataFrame({
    "Mês": meses,
    "Valor": dados[cliente]
})

# Editar valores
st.subheader("Dados do cliente")

tabela = st.data_editor(
    tabela,
    hide_index=True,
    disabled=["Mês"],
    key=f"editor_{cliente}"
)

valores = tabela["Valor"].tolist()

# Indicadores
st.subheader("Indicadores")

col1, col2, col3 = st.columns(3)

col1.metric("Total", round(sum(valores), 2))
col2.metric("Média", round(sum(valores) / len(valores), 2))
col3.metric("Maior valor", max(valores))

# Selecionar gráfico
st.subheader("Visualização dos resultados")

tipo = st.radio(
    "Tipo de gráfico:",
    ["Barras", "Linha"],
    horizontal=True
)

# Criar gráfico
fig, ax = plt.subplots(figsize=(10, 4))

fig.patch.set_facecolor("black")
ax.set_facecolor("black")

if tipo == "Barras":
    ax.bar(meses, valores, color="red")
else:
    ax.plot(
        meses,
        valores,
        color="red",
        marker="o",
        linewidth=2
    )

ax.set_title(cliente, color="white", fontsize=16)
ax.set_xlabel("Meses", color="white")
ax.set_ylabel("Valores", color="white")

ax.tick_params(colors="white")

for borda in ax.spines.values():
    borda.set_color("white")

ax.grid(axis="y", color="gray", alpha=0.3)
ax.set_axisbelow(True)

st.pyplot(fig)
plt.close(fig)

# Exportar para Excel
st.subheader("Exportar resultados")

arquivo = BytesIO()

with pd.ExcelWriter(arquivo, engine="openpyxl") as writer:
    tabela.to_excel(
        writer,
        sheet_name="Resultados",
        index=False
    )

st.download_button(
    label="📥 Baixar Excel",
    data=arquivo.getvalue(),
    file_name=f"resultado_{cliente.replace(' ', '_')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.success("Painel carregado com sucesso!")
