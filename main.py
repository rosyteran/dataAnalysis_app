import streamlit as st
import matplotlib.pyplot as plt
from retail import run_retail_analysis
from wholesale import run_wholesale_analysis

st.title("Data Analysis Dashboard")

option = st.selectbox('Which dataset would you like to analyze?', ('Retail', 'Wholesale'))
threshold = st.number_input("Enter the threshold amount:", value=500, step=100)

if st.button("Analyze"):
    if option == 'Retail':
        monthly_counts, unique_accounts = run_retail_analysis(threshold)

        # Plotting and displaying for Retail
        plt.figure(figsize=(12, 6))
        monthly_counts.plot(kind='bar', color='skyblue')
        plt.title(f"Number of Accounts Ordering ${threshold}+ per Month")
        plt.xlabel('Month')
        plt.ylabel('Number of Accounts')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        st.pyplot(plt.gcf())
        st.write("Unique Accounts Meeting the Criterion")
        st.write(unique_accounts, height=300)

    elif option == 'Wholesale':
        monthly_counts, unique_accounts, unique_product_counts_monthly = run_wholesale_analysis(threshold)

        # Check for empty data before plotting
        if not monthly_counts.empty:
            # Plotting and displaying for Wholesale
            plt.figure(figsize=(12, 6))
            monthly_counts.plot(kind='bar', color='skyblue')
            plt.title(f"Number of Accounts Ordering ${threshold}+ per Month")
            plt.xlabel('Month')
            plt.ylabel('Number of Accounts')
            plt.xticks(rotation=45)
            plt.grid(axis='y')
            st.pyplot(plt.gcf())
            st.write("Unique Accounts Meeting the Criterion")
            st.write(unique_accounts)
            st.write("Unique Product Counts Monthly for Accounts Meeting the Criterion")
            st.write(unique_product_counts_monthly)
        else:
            st.write(f"No records found for the threshold amount of ${threshold}. Try a different threshold.")
