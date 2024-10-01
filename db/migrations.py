import pandas as pd
from sqlalchemy import create_engine
import os

df = pd.read_csv("Export.csv", encoding='ISO-8859-1')
engine = create_engine(
    f'mysql+pymysql://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}@'
    f'{os.getenv("DATABASE_HOST")}/{os.getenv("DATABASE_NAME")}'
)
columns = ['FMID', 'MarketName', 'State', 'city', 'zip', 'x', 'y']
df =  df[columns]
df.rename(columns={
    'FMID': 'id',              # Assuming FMID is a unique identifier
    'MarketName': 'name',
    'State': 'state',
    'city': 'city',
    'zip': 'postal_code',
    'x': 'latitude',
    'y': 'longitude'
}, inplace=True)

#long_cities = df[df['city'].str.len() > 200]
#print(long_cities[['city']])
#df['city'] = df['city'].str.slice(0, 200)

df['latitude'] = df['latitude'].fillna(0)  # Fill missing latitude with 0
df['longitude'] = df['longitude'].fillna(0)  # Fill missing longitude with 0
df['city'] = df['city'].fillna('Unknown')  # Replace with 'Unknown' or any other placeholder
df['state'] = df['state'].fillna('Unknown')  

existing_ids = pd.read_sql('SELECT id FROM markets', con=engine)['id'].tolist()

new_records = df[~df['id'].isin(existing_ids)]

# Step 3: Insert the new records into the database if there are any
if not new_records.empty:
    new_records[['id', 'name', 'city', 'state', 'postal_code', 'latitude', 'longitude']].to_sql(
        'markets', 
        con=engine, 
        if_exists='append', 
        index=False
    )


#Index(['FMID', 'MarketName', 'Website', 'Facebook', 'Twitter', 'Youtube',
#       'OtherMedia', 'street', 'city', 'County', 'State', 'zip', 'Season1Date',
#       'Season1Time', 'Season2Date', 'Season2Time', 'Season3Date',
#       'Season3Time', 'Season4Date', 'Season4Time', 'x', 'y', 'Location',
#       'Credit', 'WIC', 'WICcash', 'SFMNP', 'SNAP', 'Organic', 'Bakedgoods',
#       'Cheese', 'Crafts', 'Flowers', 'Eggs', 'Seafood', 'Herbs', 'Vegetables',
#       'Honey', 'Jams', 'Maple', 'Meat', 'Nursery', 'Nuts', 'Plants',
#       'Poultry', 'Prepared', 'Soap', 'Trees', 'Wine', 'Coffee', 'Beans',
#       'Fruits', 'Grains', 'Juices', 'Mushrooms', 'PetFood', 'Tofu',
#       'WildHarvested', 'updateTime'],