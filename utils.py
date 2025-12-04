import pandas as pd

def adapt_dataset(df):
    df['Datetime (UTC)'] = pd.to_datetime(df['Datetime (UTC)'], format='%m/%d/%Y')
    df = df.rename(columns={
        'Datetime (UTC)': 'Timestamp',
        'Carbon intensity gCO₂eq/kWh (direct)': 'CI'
    })
    
    # Add hour based on row order within each date
    df['hour'] = df.groupby(df['Timestamp'].dt.date).cumcount()
    
    # Create proper datetime with hours
    df['Timestamp'] = df['Timestamp'] + pd.to_timedelta(df['hour'], unit='h')
    
    return df[['Timestamp', 'CI']].sort_values('Timestamp').reset_index(drop=True)
