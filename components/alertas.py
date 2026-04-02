import streamlit as st
import pandas as pd

def mostrar_alertas(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    df["stock_actual"]      = pd.to_numeric(df["stock_actual"], errors="coerce").fillna(0)
    df["stock_minimo"]      = pd.to_numeric(df["stock_minimo"], errors="coerce").fillna(0)
    df["precio_unitario"]   = pd.to_numeric(df["precio_unitario"], errors="coerce").fillna(0)
    df["unidades_vendidas"] = pd.to_numeric(df["unidades_vendidas"], errors="coerce").fillna(0)

    criticos = df[df["stock_actual"] <= df["stock_minimo"]].copy()

    if len(criticos) == 0:
        st.success("✅ Todos los productos tienen stock suficiente")
        return

    st.markdown(f"""
    <div style="background:#FEF2F2; border:1px solid #FECACA; border-radius:12px; padding:16px 20px; margin-bottom:8px;">
        <p style="margin:0; color:#991B1B; font-size:14px; font-weight:600;">
            🚨 {len(criticos)} producto(s) con stock crítico — requieren reposición
        </p>
    </div>
    """, unsafe_allow_html=True)

    for _, row in criticos.iterrows():
        nivel = row["stock_actual"] / row["stock_minimo"] if row["stock_minimo"] > 0 else 0
        color = "#EF4444" if nivel == 0 else "#F59E0B"
        st.markdown(f"""
        <div style="background:white; border:1px solid #E2E8F0; border-left:4px solid {color};
                    border-radius:10px; padding:12px 16px; margin-bottom:8px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <p style="margin:0; font-weight:600; color:#0F2044; font-size:13px;">{row['producto']}</p>
                    <p style="margin:0; color:#64748B; font-size:12px;">{row['categoria']}</p>
                </div>
                <div style="text-align:right;">
                    <p style="margin:0; color:{color}; font-weight:700; font-size:16px;">{int(row['stock_actual'])} uds</p>
                    <p style="margin:0; color:#94A3B8; font-size:11px;">Mínimo: {int(row['stock_minimo'])} uds</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def mostrar_tabla(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    df["stock_actual"]      = pd.to_numeric(df["stock_actual"], errors="coerce").fillna(0)
    df["precio_unitario"]   = pd.to_numeric(df["precio_unitario"], errors="coerce").fillna(0)
    df["unidades_vendidas"] = pd.to_numeric(df["unidades_vendidas"], errors="coerce").fillna(0)
    df["stock_minimo"]      = pd.to_numeric(df["stock_minimo"], errors="coerce").fillna(0)

    df["Valor S/"] = (df["stock_actual"] * df["precio_unitario"]).apply(lambda x: f"S/ {x:,.0f}")
    df["Precio"]   = df["precio_unitario"].apply(lambda x: f"S/ {x:,.0f}")

    def estado(row):
        if row["stock_actual"] == 0:                     return "🔴 Sin stock"
        elif row["stock_actual"] <= row["stock_minimo"]: return "🟡 Crítico"
        else:                                             return "🟢 Normal"

    df["Estado"] = df.apply(estado, axis=1)
    tabla = df[["producto","categoria","stock_actual","Precio","Valor S/","unidades_vendidas","Estado"]]
    tabla.columns = ["Producto","Categoría","Stock","Precio","Valor","Vendidos","Estado"]
    st.dataframe(tabla, use_container_width=True, hide_index=True)
