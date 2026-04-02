import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

AZUL    = "#2563EB"
ROJO    = "#EF4444"
VERDE   = "#10B981"
AMARILLO= "#F59E0B"

def grafico_stock_categorias(df):
    resumen = df.groupby("categoria")["stock_actual"].sum().reset_index()
    resumen = resumen.sort_values("stock_actual", ascending=True)
    colores = [AZUL if i == len(resumen)-1 else "#93C5FD" for i in range(len(resumen))]
    fig = go.Figure(go.Bar(
        x=resumen["stock_actual"], y=resumen["categoria"],
        orientation="h",
        marker=dict(color=colores, line=dict(width=0)),
        text=resumen["stock_actual"].apply(lambda x: f"{x} uds"),
        textposition="outside",
        textfont=dict(size=12, color="#0F2044")
    ))
    fig.update_layout(
        height=280, plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9", showticklabels=False),
        yaxis=dict(showgrid=False),
        margin=dict(l=10, r=60, t=20, b=10),
        bargap=0.35
    )
    st.plotly_chart(fig, use_container_width=True)

def grafico_mas_vendidos(df):
    top = df.nlargest(8, "unidades_vendidas")[["producto", "unidades_vendidas"]]
    top = top.sort_values("unidades_vendidas", ascending=True)
    fig = go.Figure(go.Bar(
        x=top["unidades_vendidas"], y=top["producto"],
        orientation="h",
        marker=dict(color=VERDE, line=dict(width=0)),
        text=top["unidades_vendidas"].apply(lambda x: f"{x} uds"),
        textposition="outside",
        textfont=dict(size=11, color="#0F2044")
    ))
    fig.update_layout(
        height=320, plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9", showticklabels=False),
        yaxis=dict(showgrid=False),
        margin=dict(l=10, r=60, t=20, b=10),
        bargap=0.3
    )
    st.plotly_chart(fig, use_container_width=True)

def grafico_valor_categoria(df):
    df = df.copy()
    df["valor"] = df["stock_actual"] * df["precio_unitario"]
    resumen = df.groupby("categoria")["valor"].sum().reset_index()
    fig = px.pie(
        values=resumen["valor"], names=resumen["categoria"],
        hole=0.6,
        color_discrete_sequence=[AZUL, VERDE, AMARILLO, ROJO]
    )
    fig.update_traces(textposition="outside", textinfo="percent+label",
                      marker=dict(line=dict(color="white", width=2)))
    fig.update_layout(
        height=300, paper_bgcolor="white", showlegend=False,
        margin=dict(l=10, r=10, t=20, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)
