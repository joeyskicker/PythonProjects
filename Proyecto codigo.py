# Análisis Completo de Ventas con Python (Jupyter Notebook)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.preprocessing import StandardScaler
from datetime import datetime

# Cargar datos
file_path = r"C:\Users\pepea\OneDrive\Desktop\Cibertec\Ciclo 5\Proyecto Integrador\Proyecto\tabla proyecto final.csv"
df = pd.read_csv(file_path, sep=';', na_values=["", " ", "NA", "N/A", "nan"])

# Limpieza inicial
print("/n Datos antes de limpieza:", df.shape)
df.drop_duplicates(inplace=True)
df.dropna(subset=['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID'], inplace=True)
df = df[df['Quantity'] > 0]
df = df[df['UnitPrice'] > 0]

# Conversión de tipos
print("Datos después de limpieza:", df.shape)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
df['Total'] = df['Quantity'] * df['UnitPrice']

# --- PREGUNTAS DE NEGOCIO ---

# 1. Productos más vendidos
productos_mas_vendidos = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
print("Productos más vendidos:\n", productos_mas_vendidos)

# 2. Clientes que generan más ingresos
clientes_mas_ingresos = df.groupby('CustomerID')['Total'].sum().sort_values(ascending=False).head(10)
print("Clientes con más ingresos:\n", clientes_mas_ingresos)

# 3. Productos con mayor margen (usaremos UnitPrice como aproximado)
productos_margen = df.groupby('Description')['UnitPrice'].mean().sort_values(ascending=False).head(10)
print("Productos con mayor precio promedio (aprox. margen):\n", productos_margen)

# 4. Productos que menos se venden
productos_menos_vendidos = df.groupby('Description')['Quantity'].sum().sort_values().head(10)
print("Productos menos vendidos:\n", productos_menos_vendidos)

# 5. Patrones mensuales
df['Mes'] = df['InvoiceDate'].dt.month
df['Año'] = df['InvoiceDate'].dt.year
ventas_mensuales = df.groupby(['Año', 'Mes'])['Total'].sum()
ventas_mensuales.plot(title="Ventas por Mes")
plt.show()

# 6. Ticket promedio
ticket_promedio = df.groupby('InvoiceNo')['Total'].sum().mean()
print("Ticket promedio por factura:", round(ticket_promedio, 2))

# 7. Productos que se compran juntos (reglas de asociación)
df_basket = (df[df['Country'] == "United Kingdom"]
             .groupby(['InvoiceNo', 'Description'])['Quantity']
             .sum().unstack().fillna(0).gt(0))  # reemplazado applymap con gt(0)

frequent_itemsets = apriori(df_basket, min_support=0.01, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
print("Reglas de productos comprados juntos:\n", rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head())

# 8. Clientes que dejaron de comprar (churn)
ultima_fecha = df['InvoiceDate'].max()
recencia = df.groupby('CustomerID')['InvoiceDate'].max().apply(lambda x: (ultima_fecha - x).days)
clientes_churn = recencia[recencia > 90].sort_values(ascending=False).head(10)
print("Clientes potencialmente churn:\n", clientes_churn)

# 9. Día/Hora con más ventas
df['Hora'] = df['InvoiceDate'].dt.hour
ventas_hora = df.groupby('Hora')['Total'].sum()
ventas_hora.plot(kind='bar', title="Ventas por Hora")
plt.show()

# 10. Frecuencia de compra por cliente
frecuencia = df.groupby('CustomerID')['InvoiceNo'].nunique().sort_values(ascending=False)
print("Frecuencia de compra por cliente (top 5):\n", frecuencia.head())

# 11. Productos con más devoluciones (InvoiceNo que comienza con 'C')
devoluciones = df[df['InvoiceNo'].astype(str).str.startswith('C')]
productos_devueltos = devoluciones.groupby('Description')['Quantity'].sum().abs().sort_values(ascending=False).head(10)
print("Productos con más devoluciones:\n", productos_devueltos)

# 12. País con más ventas
ventas_pais = df.groupby('Country')['Total'].sum().sort_values(ascending=False).head(10)
print("Ventas por país:\n", ventas_pais)

# 13. Tasa de retorno por país
devoluciones_pais = devoluciones.groupby('Country')['Total'].sum().abs()
total_ventas_pais = df.groupby('Country')['Total'].sum()
tasa_retorno = (devoluciones_pais / total_ventas_pais).dropna().sort_values(ascending=False)
print("Tasa de retorno por país:\n", tasa_retorno)

# 14. Productos con ventas estacionales
ventas_por_mes = df.groupby(['Description', 'Mes'])['Quantity'].sum().unstack().fillna(0)
productos_estacionales = ventas_por_mes.std(axis=1).sort_values(ascending=False).head(10)
print("Productos con mayor variabilidad mensual:\n", productos_estacionales)

# 15. Volumen de ventas semanal
df['Semana'] = df['InvoiceDate'].dt.isocalendar().week
ventas_semanal = df.groupby(['Año', 'Semana'])['Total'].sum()
ventas_semanal.plot(title="Ventas Semanales")
plt.show()

# 16. Clientes que deben recibir ofertas personalizadas (menos ingresos y frecuencia baja)
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (ultima_fecha - x.max()).days,
    'InvoiceNo': 'nunique',
    'Total': 'sum'
})
rfm.columns = ['Recency', 'Frequency', 'Monetary']
clientes_oferta = rfm.sort_values(['Recency', 'Frequency', 'Monetary'], ascending=[False, True, True]).head(10)
print("Clientes recomendados para ofertas:\n", clientes_oferta)
