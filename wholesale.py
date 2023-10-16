import pandas as pd
import re

def run_wholesale_analysis(threshold):
    df_wholesale = pd.read_csv('wholesale.csv')

    # Extraction functions
    email_pattern = r"'email':\s*'([^']+)'"
    id_pattern = r"'id':\s*(\d+)"
    first_name_pattern = r"'first_name':\s*'([^']+)'"
    last_name_pattern = r"'last_name':\s*'([^']+)'"

    df_wholesale['email_extracted'] = df_wholesale['customer'].apply(
        lambda x: re.search(email_pattern, str(x)).group(1) if pd.notnull(x) and re.search(email_pattern, str(x)) else None
    )
    df_wholesale['user_id'] = df_wholesale['customer'].apply(
        lambda x: int(re.search(id_pattern, str(x)).group(1)) if pd.notnull(x) and re.search(id_pattern, str(x)) else None
    )
    df_wholesale['first_name_extracted'] = df_wholesale['billing_address'].apply(
        lambda x: re.search(first_name_pattern, str(x)).group(1) if pd.notnull(x) and re.search(first_name_pattern, str(x)) else None
    )
    df_wholesale['last_name_extracted'] = df_wholesale['billing_address'].apply(
        lambda x: re.search(last_name_pattern, str(x)).group(1) if pd.notnull(x) and re.search(last_name_pattern, str(x)) else None
    )

    df_wholesale['created_at'] = pd.to_datetime(df_wholesale['created_at'], utc = True)
    df_wholesale['month_year'] = df_wholesale['created_at'].dt.tz_localize(None).dt.to_period('M')

    filtered_data = df_wholesale[df_wholesale['total_price'] >= threshold]
    monthly_counts = filtered_data.groupby('month_year')['user_id'].nunique()
    
    unique_accounts = filtered_data[['user_id', 'email_extracted', 'first_name_extracted', 'last_name_extracted']].drop_duplicates()
    unique_product_counts_monthly = filtered_data.groupby(['user_id', 'month_year'])['name'].nunique().reset_index()
    unique_product_counts_monthly.columns = ['User ID', 'Month-Year', 'Unique Product Count']
    
    return monthly_counts, unique_accounts, unique_product_counts_monthly
