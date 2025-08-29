from flask import Flask, render_template
import pymongo, os
from pymongo.errors import ServerSelectionTimeoutError


app = Flask(__name__)

# Get Mongo connection string from env (defaults to in-cluster name)
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://mongodb:27017")
DB_NAME = os.getenv("MONGODB_DB", "messages")
COLLECTION = os.getenv("MONGODB_COLLECTION", "check")

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
col = db[COLLECTION]

@app.route('/')
def index():
    
    try:
        # ensure there's at least  one document
        client.admin.command("ping")
        doc = col.find_one()
        if not doc:
            col.insert_one({"message": "hello from mongodb"})
            doc = col.find_one()
        return doc.get("message", "no message in db")
    
    except ServerSelectionTimeoutError as e:
        return f"database unavailable: {e}", 503

# health check route
@app.route('/healthz', methods=['GET'])
def health():
    return 'ok', 200

if __name__ == '__main__':
    app.run(debug=True,port=80,host='0.0.0.0')