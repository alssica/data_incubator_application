from flask import Flask
from flask import render_template
from pymongo import MongoClient

import json
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)

# mongodb data
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'corp_miscon'
COLLECTION_NAME = 'projects'
FIELDS = {"Company":True, "Parent Company":True, "Penalty Amount":True, "Penalty Year": True, "Penalty Date":True, "Ownership Structure":True, "Major Industry of Parent":True, "Specific Industry of Parent":True, "Primary Offense":True, "Secondary Offense":True, "Agency":True, "Lawsuit Resolution":True, "Facility State":True, "Civil/Criminal":True, "_id":False}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/corp_miscon/projects")
def copr_miscon_projects():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    projects = collection.find(projection=FIELDS, limit=5000)
    # projects = collection.find({} ,FIELDS)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects

if __name__ == "__main__":
    app.run()
