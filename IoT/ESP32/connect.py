from datetime import datetime
import pandas as pd
import pymongo
import pytz
from flask import Flask, jsonify, request

app = Flask(_name_)

uri = "mongodb://ohmaigot:22omgpro@ac-x32m9gw-shard-00-00.kfniqpk.mongodb.net:27017,ac-x32m9gw-shard-00-01.kfniqpk.mongodb.net:27017,ac-x32m9gw-shard-00-02.kfniqpk.mongodb.net:27017/?ssl=true&replicaSet=atlas-13lmid-shard-0&authSource=admin&retryWrites=true&w=majority&appName=ohmaigot-cluster"
client = pymongo.MongoClient(uri)
db = client['IoTDatabase']
collection = db['Sensor']

@app.route("/")
def root():
    """Route data telah tersimpan di MongoDB"""
    data = [x for x in collection.find()]
    df = pd.DataFrame.from_dict(data)
    return df.to_html(), 200

@app.route("/temperature/all")
def get_all_temperature():
    """Route menampilkan semua data temperature"""
    data = [x ["temperature"] for x in collection.find()]
    return data

@app.route("/temperature/avg")
def get_avg_temperature():
    """Route menampilkan rata-rata data temperature"""
    data = [x ["temperature"] for x in collection.find()]
    avg = sum(data)/len(data)
    return jsonify("average temperature: ", avg)

@app.route("/humidity/all")
def get_all_humidity():
    """Route menampilkan semua data humidity"""
    data = [x ["humidity"] for x in collection.find()]
    return data

@app.route("/humidity/avg")
def get_avg_humidity():
    """Route menampilkan rata-rata data humidity"""
    data = [x ["humidity"] for x in collection.find()]
    avg = sum(data)/len(data)
    return jsonify("average humidity: ", avg)

@app.route("/sensor", methods=["POST"])
def post_sensor():
    """Route untuk memasukkan dengan method POST
    data dimasukkan dalam bentuk JSON di body pesan"""
    timestamp = datetime.now(tz=pytz.timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S")
    temp = float(request.json["temperature"])
    hum = float(request.json["humidity"])
    new_data = {"temperature": temp, "humidity": hum, "timestamp": timestamp}
    collection.insert_one(new_data.copy())
    return jsonify(new_data)

if _name_ == "_main_":
    app.run(host='0.0.0.0', port=5000, debug=True)