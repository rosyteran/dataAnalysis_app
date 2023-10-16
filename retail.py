import pandas as pd

def run_retail_analysis(threshold):
    df_retail = pd.read_csv('retail_chunk.csv', encoding='ISO-8859-1')
    df_retail['Created at'] = df_retail['Created at'].apply(lambda x: pd.to_datetime(x, utc=True))
    df_retail['month_year'] = df_retail['Created at'].dt.strftime('%b %Y')

    filtered_data = df_retail[df_retail['Total'] >= threshold]
    monthly_counts = filtered_data.groupby('month_year')['Name'].nunique()
    unique_accounts = filtered_data[['Name', 'Email']].drop_duplicates()

    return monthly_counts, unique_accounts
