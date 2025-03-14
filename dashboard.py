import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
# from babel.numbers import format_currency

sns.set(style='dark')
st.set_page_config(page_title="Analisis E-Commerce Public Dataset", layout="wide")

st.sidebar.markdown("## Navigasi")
if st.sidebar.button("Halaman Utama"):
    menu = "Halaman Utama"
elif st.sidebar.button("Analisis Data"):
    menu = "Analisis Data"
else:
    menu = "Halaman Utama"

if menu == "Halaman Utama":
    st.markdown("""
        <h1 style='text-align: center;'>Analisis E-Commerce Public Dataset</h1>
        <h3 style='text-align: center;'>Berikut adalah dataset yang digunakan pada Analisis Data kali ini</h3>
        """, unsafe_allow_html=True)
    
    dataset_options = {"Category Reviews": "category_reviews.csv", 
                       "Ordered Products": "ordered_products_by_customers.csv",
                       }
    selected_dataset = st.selectbox("Pilih Dataset:", list(dataset_options.keys()))
    file_path = dataset_options[selected_dataset]

    df = pd.read_csv(file_path)


    st.write(f"### Dataframe yang Dipilih: {selected_dataset}")
    st.dataframe(df)


elif menu == "Analisis Data":
    st.markdown("""
        <h1 style='text-align: center;'>📊 Analisis Data</h1>
    """, unsafe_allow_html=True)

    # PERTANYAAN 1
    st.write("")
    st.write("### PERTANYAAN 1")
    st.write("###  Produk apa saja yang memiliki volume pembelian tertinggi?")

    ordered_products_by_customers_df = pd.read_csv("ordered_products_by_customers.csv")
    # datetime_columns = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
    ordered_products_by_customers_df.reset_index(inplace=True)

    # for column in datetime_columns:
    #     ordered_products_by_customers_df[column] = pd.to_datetime(ordered_products_by_customers_df[column])

    ordered_products_by_customers_df["product_category_name"] = ordered_products_by_customers_df["product_category_name"].astype(str)


    # print(ordered_products_by_customers_df.product_category_name.info())

    top_10_products = ordered_products_by_customers_df.groupby(by="product_category_name", as_index=False).agg({
        "order_id": "nunique",
        "price_y": "sum"
    }).nlargest(10, "order_id")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_10_products["product_category_name"], top_10_products["order_id"], color="skyblue")

    ax.set_title("Top 10 Best Selling Products", loc="center", fontsize=20)
    ax.set_xlabel('Total Sales')
    ax.set_ylabel('Product Category Name')
    ax.invert_yaxis()
    st.pyplot(fig)

    st.write("### Best Selling Product:")
    st.dataframe(top_10_products)

    st.write("")
    st.write("")
    # PERTANYAAN 2
    st.write("### PERTANYAAN 2")
    st.write("###  Apa kategori produk yang memiliki rating tertinggi dan rating terendah?  ")
    category_reviews_df = pd.read_csv("category_reviews.csv")

    category_reviews_sorted = category_reviews_df.sort_values(by="review_score", ascending=False)
    top_10_products_by_review = category_reviews_sorted.head(10)
    top_10_lowest_rating_products = category_reviews_sorted.tail(10)

    top_10_products_by_review["Kategori"] = "Top 10"
    top_10_lowest_rating_products["Kategori"] = "Lowest 10"
    combined_data = pd.concat([top_10_products_by_review, top_10_lowest_rating_products])
                            
    fig, ax = plt.subplots(figsize=(18, 6))
    sns.scatterplot(
        x=combined_data["product_category_name_english"],
        y=combined_data["review_score"],
        hue=combined_data["Kategori"],
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

    st.write("### Top Rated Product:  ")
    st.dataframe(top_10_products_by_review)

    st.write("### Lowest Rated Product:  ")
    st.dataframe(top_10_lowest_rating_products)