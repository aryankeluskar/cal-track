from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import pytz
from tzlocal import get_localzone
from functools import lru_cache

load_dotenv()

# MongoDB connection - use connection pooling
client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'),
                    maxPoolSize=10,
                    serverSelectionTimeoutMS=5000)
db = client['calorie_tracker']
food_entries = db['food_entries']

# Create indexes for better performance
food_entries.create_index([("timestamp", -1)])

@lru_cache(maxsize=1)
def get_local_timezone():
    return get_localzone()

def add_food_entry(calories, carbs, protein):
    entry = {
        'timestamp': datetime.now(get_local_timezone()),
        'calories': calories,
        'carbs': carbs,
        'protein': protein
    }
    return food_entries.insert_one(entry)

def get_food_entries(limit=50):
    local_tz = get_local_timezone()
    last_24h = datetime.now(local_tz) - timedelta(days=1)
    
    # Use the index we created
    cursor = food_entries.find(
        {'timestamp': {'$gte': last_24h}},
        {'_id': 0}
    ).sort('timestamp', -1).limit(limit)
    
    return list(cursor)

def get_daily_totals():
    local_tz = get_local_timezone()
    last_24h = datetime.now(local_tz) - timedelta(days=1)
    
    # More efficient aggregation pipeline
    pipeline = [
        {
            '$match': {
                'timestamp': {'$gte': last_24h}
            }
        },
        {
            '$group': {
                '_id': None,
                'calories': {'$sum': '$calories'},
                'carbs': {'$sum': '$carbs'},
                'protein': {'$sum': '$protein'}
            }
        },
        {
            '$project': {
                '_id': 0,
                'calories': 1,
                'carbs': 1,
                'protein': 1
            }
        }
    ]
    
    result = list(food_entries.aggregate(pipeline))
    if result:
        return result[0]
    return {'calories': 0, 'carbs': 0, 'protein': 0} 