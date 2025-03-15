import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')
st.set_page_config(page_title="Analisis E-Commerce Public Dataset", layout="wide")

st.markdown("""
    <h1 style='text-align: center;'>📊 Analisis Data</h1>
""", unsafe_allow_html=True)

# ------------------------
# PERTANYAAN 1
# ------------------------
st.write("")
st.write("### PERTANYAAN 1")
st.write("###  Produk apa saja yang memiliki volume pembelian tertinggi?")

# 1) Baca data
try:
    ordered_products_by_customers_df = pd.read_csv("ordered_products_by_customers.csv")
except FileNotFoundError:
    st.error("File 'ordered_products_by_customers.csv' tidak ditemukan!")
    st.stop()

# 2) Convert kolom tanggal menjadi datetime
datetime_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]
for col in datetime_columns:
    if col in ordered_products_by_customers_df.columns:
        ordered_products_by_customers_df[col] = pd.to_datetime(
            ordered_products_by_customers_df[col], errors='coerce'
        )

# 3) Pastikan kolom product_category_name bertipe string
if "product_category_name" in ordered_products_by_customers_df.columns:
    ordered_products_by_customers_df["product_category_name"] = (
        ordered_products_by_customers_df["product_category_name"].astype(str)
    )

# 4) Pastikan kolom order_delivered_customer_date ada dan valid
if "order_delivered_customer_date" not in ordered_products_by_customers_df.columns:
    st.error("Kolom 'order_delivered_customer_date' tidak ditemukan di dataset.")
    st.stop()

# 5) Dapatkan tahun terkecil dan terbesar
#    Pastikan juga kolom sudah datetime (di langkah 2)
min_year = int(ordered_products_by_customers_df["order_delivered_customer_date"].dt.year.min())
max_year = int(ordered_products_by_customers_df["order_delivered_customer_date"].dt.year.max())

if pd.isna(min_year) or pd.isna(max_year):
    st.error("Nilai tahun di kolom 'order_delivered_customer_date' tidak valid.")
    st.stop()

# 6) Pilih rentang tahun (start_year hingga end_year)
start_year, end_year = st.slider(
    label='Rentang Tahun',
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# 7) Filter data berdasarkan rentang tahun
mask = (
    (ordered_products_by_customers_df["order_delivered_customer_date"].dt.year >= start_year) &
    (ordered_products_by_customers_df["order_delivered_customer_date"].dt.year <= end_year)
)
filtered_df = ordered_products_by_customers_df[mask].copy()

# 8) Pastikan kolom 'price_y' ada (untuk agg sum harga)
if "price_y" not in filtered_df.columns:
    st.error("Kolom 'price_y' tidak ada. Harap sesuaikan dengan kolom harga yang benar.")
    st.stop()

# 9) Hitung top 10 produk (berdasarkan jumlah unique order)
top_10_products = (
    filtered_df
    .groupby("product_category_name", as_index=False)
    .agg({
        "order_id": "nunique",
        "price_y": "sum"
    })
    .nlargest(10, "order_id")  # ambil 10 terbesar
)

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top_10_products["product_category_name"], top_10_products["order_id"], color="skyblue")
ax.set_title("Top 10 Best Selling Products", loc="center", fontsize=20)
ax.set_xlabel('Total Sales')
ax.set_ylabel('Product Category Name')
ax.invert_yaxis()
st.pyplot(fig)

st.write("### Best Selling Product:")
st.dataframe(top_10_products)

# ------------------------
# PERTANYAAN 2
# ------------------------
st.write("")
st.write("### PERTANYAAN 2")
st.write("###  Apa kategori produk yang memiliki rating tertinggi dan rating terendah?")

try:
    category_reviews_df = pd.read_csv("category_reviews.csv")
except FileNotFoundError:
    st.error("File 'category_reviews.csv' tidak ditemukan!")
    st.stop()

# Pastikan kolom review_score ada dan bertipe numeric
if "review_score" not in category_reviews_df.columns:
    st.error("Kolom 'review_score' tidak ada di 'category_reviews.csv'.")
    st.stop()
category_reviews_df["review_score"] = pd.to_numeric(category_reviews_df["review_score"], errors='coerce')

# Urutkan berdasarkan review_score descending
category_reviews_sorted = category_reviews_df.sort_values(by="review_score", ascending=False)

# Ambil 10 tertinggi dan 10 terendah
top_10_products_by_review = category_reviews_sorted.head(10).copy()
top_10_lowest_rating_products = category_reviews_sorted.tail(10).copy()

# Tambahkan kolom 'Kategori' untuk memudahkan penandaan di scatter plot
top_10_products_by_review["Kategori"] = "Top 10"
top_10_lowest_rating_products["Kategori"] = "Lowest 10"
combined_data = pd.concat([top_10_products_by_review, top_10_lowest_rating_products])

fig, ax = plt.subplots(figsize=(18, 6))
# Pastikan kolom 'product_category_name_english' ada di dataset
if "product_category_name_english" not in combined_data.columns:
    st.error("Kolom 'product_category_name_english' tidak ditemukan di 'category_reviews.csv'.")
    st.stop()

sns.scatterplot(
    data=combined_data,
    x="product_category_name_english",
    y="review_score",
    hue="Kategori",
    palette={"Top 10": "green", "Lowest 10": "red"},
    s=100,
    ax=ax
)

plt.xticks(rotation=45)
plt.title("Scatter Plot: Produk dengan Review Tertinggi & Terendah", fontsize=14)
plt.xlabel("Kategori Produk", fontsize=12)
plt.ylabel("Skor Review", fontsize=12)
plt.legend(title="Kategori", loc="upper right")

st.pyplot(fig)

st.write("### Top Rated Product:")
st.dataframe(top_10_products_by_review)

st.write("### Lowest Rated Product:")
st.dataframe(top_10_lowest_rating_products)
