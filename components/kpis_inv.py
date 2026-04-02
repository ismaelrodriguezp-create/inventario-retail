import streamlit as st

def mostrar_kpis_inv(df):
    total_productos = len(df)
    valor_inventario = (df["stock_actual"] * df["precio_unitario"]).sum()
    productos_criticos = len(df[df["stock_actual"] <= df["stock_minimo"]])
    total_vendidos = df["unidades_vendidas"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Total productos",     f"{total_productos}")
    col2.metric("💰 Valor inventario",    f"S/ {valor_inventario:,.0f}")
    col3.metric("🚨 Stock crítico",       f"{productos_criticos} productos", delta=f"-{productos_criticos} alertas", delta_color="inverse")
    col4.metric("🛒 Unidades vendidas",   f"{total_vendidos:,}")
