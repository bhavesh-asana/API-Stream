# Course: Advanced Database Systems (CRN-23223)
# Author: Bhavesh Asanabada (#700744873)

# ----------- Mongo Connection --------------
# Connection        : localhost
# Transmission port : 27017 (default port)
# Database name     : "database"
# Collection name   : "hulu"
# -------------------------------------------

# Import statements
from pymongo import MongoClient


# Function to connect with MongoDB
def mongo_connect():
    cluster = None
    try:
        # Define MongoDB instance
        # Localhost Instance
        client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=1000)

        # MongoDB Atlas: cloud Instance
        # client = MongoClient("mongodb+srv://admin:admin1234@cluster0.vb4vgsl.mongodb.net/?retryWrites=true&w=majority")
        client.server_info()

        # Define database
        cluster = client['database']

    except Exception as ex:
        print(ex)
        print("Error - Could not connect to database")

    return cluster
