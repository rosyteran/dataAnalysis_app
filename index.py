
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def convert_to_datetime(val):
    try:
        return pd.to_datetime(val,  utc = True)
    except:
        return None

# Extraction functions (adapted for the retail dataset structure)
def extract_email_from_retail(row):
    return row['Email']

def extract_user_id_from_retail(row):
    return row['Name']



# Analysis Function adapted for retail dataset
def run_analysis():

    print("Inclue")
    df_retail = pd.read_csv('retail.csv', low_memory=False)
    print("dine")

    df_retail['Created at'] = df_retail['Created at'].apply(convert_to_datetime)
    # Extracting the relevant columns
    df_retail['email_extracted'] = df_retail.apply(extract_email_from_retail, axis=1)
    df_retail['user_id'] = df_retail.apply(extract_user_id_from_retail, axis=1)

    # Streamlit interface for retail dataset
    st.title("Retail Data Analysis")
    threshold = st.number_input("Enter the threshold amount:", value=500, step=100)

    df_retail['Created at'] = pd.to_datetime(df_retail['Created at'])
    df_retail['month_year'] = df_retail['Created at'].dt.strftime('%b %Y')
    filtered_data = df_retail[df_retail['Total'] >= threshold]
    monthly_counts = filtered_data.groupby('month_year')['user_id'].nunique()
    
    # Plot with matplotlib for more control over the graph
    plt.figure(figsize=(12, 6))
    monthly_counts.plot(kind='bar', color='skyblue')
    plt.title(f"Number of Accounts Ordering ${threshold}+ per Month")
    plt.xlabel('Month')
    plt.ylabel('Number of Accounts')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    st.pyplot(plt.gcf())
    
    # Displaying user details with scrollable table
    unique_accounts = filtered_data[['user_id', 'email_extracted']].drop_duplicates()
    st.write("Unique Accounts Meeting the Criterion")
    st.write(unique_accounts, height=300)  # Setting height for scrollable display



if __name__ == "__main__":

    if st.button("Analyze Retail"):
        run_analysis()
