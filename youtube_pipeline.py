import requests
import os
import json
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine



load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')
DB_NAME = os.getenv('POSTGRES_DB')

DATABASE_URL=f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine=create_engine(DATABASE_URL)
print("Database connection established")



def get_trending_videos(api_key, region_code='US', max_results=50):
    base_url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'snippet, contentDetails, statistics',
        'chart': 'mostPopular',
        'regionCode': region_code,
        'maxResults': max_results,
        'key': api_key
        }
    try:
        response=requests.get(base_url, params=params)
        response.raise_for_status()  #It will do nothing but jump to the exception if the response is not 200
        print("API call successful")
        return response.json()  
    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
        return None
    
def transform_data(data):
    if not data or 'items' not in data:
        print("No data to transform")
        return None
    videos_data = []
    print(f"Transforming {len(data['items'])} videos data")
    for item in data['items']:
        snippet = item.get('snippet', {})
        stats= item.get('statistics', {})

        videos_info = {
            'video_id':item.get('id'),
            'title': snippet.get('title'),
            'publishedAt': snippet.get('publishedAt'),
            'channelId': snippet.get('channelId'),
            'channelTitle': snippet.get('channelTitle'),
            'categoryId': snippet.get('categoryId'),
            'viewCount': stats.get('viewCount'),
            'likeCount': stats.get('likeCount'),
            'commentCount': stats.get('commentCount'), 
           
        }

        videos_data.append(videos_info)

    if not videos_data:
        print("No videos data to transform")
        return None
        
    df=pd.DataFrame(videos_data)
    print(f"Transformed data into DataFrame with {len(df)} rows")


    print(f"cleaning date and converting types")

    #lets convert the numeric columns to int
    numeric_columns=['viewCount', 'likeCount', 'commentCount']
    for col in numeric_columns:
        df[col]= pd.to_numeric(df[col], errors='coerce') #convert to numeric(float), setting errors='coerce' will convert non-numeric values to NaN
        df[col]= df[col].astype('Int64')  # Use 'Int64' to allow for NaN values as NA
        
    df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')  # Convert to datetime, setting errors='coerce' will convert non-datetime values to NaT
    print("Data cleaned and types converted")

    return df
    
def load_data_to_db(df, table_name, db_engine):
    print(f"Loading data into {table_name} table")
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False, method='multi') #'multi' was used to batch insert the data
        print(f"Data Successfully loaded into DB")  # Load the DataFrame into the database
        return True #Confirm successful load
    except Exception as e:
        print(f"Error loading data into DB: {e}")
        return False
        
    
if __name__ == "__main__":  #we set __name__ to __main__ to make sure that this code only runs when this file is executed directly
    print("Starting the pipeline")
    data=get_trending_videos(API_KEY, region_code='US', max_results=50)

    if data:
        with open('trending_videos.json', 'w') as f:
            json.dump(data, f, indent=4)            # Write the Python dictionary (parsed JSON) to a file in JSON format, with readable indentation
        print("Data saved to trending_videos.json")

    cleaned_data=transform_data(data)

    if cleaned_data is not None:
        print("\n Cleaned Dataframe:")
        print("Dataframe Head (first 5 rows):")
        print(cleaned_data.head())
        print("\n Dataframe Info:")
        print(cleaned_data.info())

        try:
            cleaned_data.to_csv('trending_videos.csv', index=False)  # Save the DataFrame to a CSV file
            print("Data saved to trending_videos.csv")
            
            
        except Exception as e:
            print(f"Error saving DataFrame to CSV: {e}") 

        print("\n Next step: Load the data into a database.")

        table_name='trending_videos'
        load_successfull=load_data_to_db(cleaned_data, table_name, engine)  # Load the DataFrame into the database
        if load_successfull:
            print(f"Data loaded into {table_name} table in the database")
        else:
            print(f"Failed to load data into {table_name} table in the database")
    else: 
        print("No cleaned data to save.")
        print("\n Pipeline failed.")
        exit()
else:
    print("No data fetched from the API.")
    
print("Pipeline completed.")