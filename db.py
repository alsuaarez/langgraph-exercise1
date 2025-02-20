import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging
load_dotenv()

logger = logging.getLogger(__name__)

def get_database():
# Test connection
    try:
    # Get MongoDB URI from environment variable
        mongodb_uri = os.getenv("MONGO_URI")

        # create a client
        client = MongoClient(mongodb_uri)

        # Access a specific database
        db = client['test']

        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        logger.info("Successfully connected to MongoDB!")
        return db
    
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        raise



