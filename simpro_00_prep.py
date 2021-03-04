
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


monday = pd.read_csv('data/monday.csv', delimiter =';')
tuesday = pd.read_csv('data/tuesday.csv', delimiter =';' )
wednesday = pd.read_csv('data/wednesday.csv', delimiter =';')
thursday = pd.read_csv('data/thursday.csv', delimiter =';')
friday = pd.read_csv('data/friday.csv', delimiter =';')
df = pd.concat([monday, tuesday, wednesday, thursday, friday], axis = 0)

df['timestamp'] = pd.to_datetime(df['timestamp'])

conditions = [
    (df['location'] == "fruit"),
    (df['location'] == "spices"),
    (df['location'] == "dairy"),
    (df['location'] == "drinks"),
    ]

values = [4, 3, 5, 6]

df['revenue_per_minute'] = np.select(conditions, values)

df["unq_id"] = 'Cust_' + df["timestamp"].astype(str) + '_no_' + df["customer_no"].astype(str) 

df = df[['timestamp', 'unq_id', 'customer_no', 'location' , 'revenue_per_minute']]

df = df.sort_values(['customer_no', 'timestamp'])
df.set_index('timestamp', inplace=True)
df = df.groupby('unq_id').resample('1min').fillna('ffill')

df['before'] = df['location'].shift(1)

df = df.drop(columns=['unq_id'])

df.to_csv('data/df_prepped.csv', index=True)

trans_prob = pd.crosstab(df['location'], df['before'], normalize=0)

trans_prob.to_csv('data/trans_matrix_prob.csv', index=True)

