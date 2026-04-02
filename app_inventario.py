import streamlit as st
import pandas as pd
from components.kpis_inv import mostrar_kpis_inv
from components.graficos_inv import grafico_stock_categorias, grafico_mas_vendidos, grafico_valor_categoria
from components.alertas import mostrar_alertas, mostrar_tabla

st.set_page_config(page_title="Inventario | Retail", page_icon="📦", layout="wide")

st.markdown("""
<style>
    .main { background-color: #F4F6FB; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    section[data-testid="stSidebar"] { background: linear-gradient(180deg, #0F2044 0%, #1B3A6B 100%); }
    section[data-testid="stSidebar"] * { color: #E2E8F0 !important; }
    div[data-testid="metric-container"] {
        background: white; border: 1px solid #E2E8F0;
        border-radius: 16px; padding: 20px 24px;
        box-shadow: 0 2px 8px rgba(15,32,68,0.06);
    }
    div[data-testid="metric-container"] label { color: #64748B !important; font-size: 13px !important; }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #0F2044 !important; font-size: 26px !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display:flex; align-items:center; gap:14px; margin-bottom:4px;">
    <div style="background:#2563EB; border-radius:14px; padding:10px 14px;">
        <span style="font-size:24px;">📦</span>
    </div>
    <div>
        <h1 style="margin:0; font-size:26px; color:#0F2044; font-weight:700;">Control de Inventario</h1>
        <p style="margin:0; color:#64748B; font-size:13px;">Tienda Retail · Gestión de stock en tiempo real</p>
    </div>
</div>
<hr style="border:none; border-top:1px solid #E2E8F0; margin:16px 0 20px;">
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<p style='font-size:11px; color:#94A3B8; font-weight:600; letter-spacing:0.08em;'>DATOS</p>", unsafe_allow_html=True)
    archivo = st.file_uploader("Subir Excel o CSV", type=["csv","xlsx"])
    st.markdown("<hr style='border-color:#1E3A5F; margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px; color:#94A3B8; font-weight:600; letter-spacing:0.08em;'>FILTROS</p>", unsafe_allow_html=True)

if archivo:
    df = pd.read_csv(archivo) if archivo.name.endswith(".csv") else pd.read_excel(archivo)
    st.sidebar.success("✓ Archivo cargado")
else:
    df = pd.read_csv("data/inventario_ejemplo.csv")
    st.sidebar.info("Usando datos de ejemplo")

cats = ["Todas"] + sorted(df["categoria"].unique().tolist())
cat_sel = st.sidebar.selectbox("Categoría", cats)
df_filtrado = df[df["categoria"] == cat_sel] if cat_sel != "Todas" else df

mostrar_kpis_inv(df_filtrado)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### 🚨 Alertas de stock crítico")
mostrar_alertas(df_filtrado)

st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 📊 Stock por categoría")
    grafico_stock_categorias(df_filtrado)
with col2:
    st.markdown("#### 🔵 Valor por categoría")
    grafico_valor_categoria(df_filtrado)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### 🛒 Productos más vendidos")
grafico_mas_vendidos(df_filtrado)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### 📋 Detalle completo de inventario")
mostrar_tabla(df_filtrado)

st.markdown("""
<hr style="border:none; border-top:1px solid #E2E8F0; margin-top:2rem;">
<p style="text-align:center; color:#94A3B8; font-size:12px;">Control de Inventario · Python & Streamlit · Desarrollado por Ismael Rodriguez</p>
""", unsafe_allow_html=True)
