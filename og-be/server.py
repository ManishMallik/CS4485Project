from sqlalchemy import text
import random
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine
app = Flask(__name__)
cors = CORS(app)
@app.route("/sendinfo")
def sendinfo():
    # model_type is {LCCDE, Tree Based, MST} dataset is {non_km, km}
    # step 1: information parsing
    model_num = int(request.args.get('model_type'))
    if model_num == 1:
        model_type = "LCCDE"
    elif model_num == 2:
        model_type = "Tree Based"
    elif model_num == 3:
        model_type = "MST"
    dataset_num = int(request.args.get('dataset'))
    if dataset_num == 1:
        dataset = "data/CICIDS2017_sample.csv"
    elif dataset_num == 2:
        dataset = "data/CICIDS2017_sample_km.csv"

    # step 2: run the selected model with the selected dataset
    # step 3: save the output to the sql database
    f = open("/home/ash/Projects/CS4485Project/og-be/.secrets", "r")
    secret = f.read().strip()
    engine = create_engine(f"mysql+pymysql://{secret}@72.182.161.176/IDS")
    dict = {}

    with engine.connect() as conn:
        conn.execute(
            text(f"INSERT INTO Results (model, benign, dos, portscan, bot, infiltration, webattack, bruteforce, dataset) VALUES ({model_num}, {random.randint(0, 100)}, {random.randint(0, 100)}, {random.randint(0, 100)}, {random.randint(0, 100)}, {random.randint(0, 100)}, {random.randint(0, 100)}, {random.randint(0, 100)}, {dataset_num})")
        )
        conn.commit()
        recent = conn.execute(text("SELECT DATE_FORMAT(time, '%Y-%m-%d %H:%i:%s') AS time, model, benign, bot, bruteforce, dataset, dos, id, infiltration, portscan, webattack FROM Results ORDER BY time DESC")).fetchall()[0];
        dict = {}
        dict["time"] = recent[0]
        dict["model"] = recent[1]
        dict["benign"] = recent[2]
        dict["bot"] = recent[3]
        dict["bruteforce"] = recent[4]
        dict["dataset"] = recent[5]
        dict["dos"] = recent[6]
        dict["id"] = recent[7]
        dict["infiltration"] = recent[8]
        dict["portscan"] = recent[9]
        dict["webattack"] = recent[10]
    # step 4: return the output to the front end
    return dict
@app.route("/getinfo")
# For past results to query all the previous results
def getinfo():
    f = open("/home/ash/Projects/CS4485Project/og-be/.secrets", "r")
    secret = f.read().strip()
    engine = create_engine(f"mysql+pymysql://{secret}@72.182.161.176/IDS")
    arr = []
    with engine.connect() as conn:
        for i in conn.execute(text("SELECT * FROM Results")).fetchall():
            dict = {}
            dict["id"] = i[0]
            dict["time"] = i[1]
            dict["model"] = i[2]
            dict["benign"] = i[3]
            dict["dos"] = i[4]
            dict["portscan"] = i[5]
            dict["bot"] = i[6]
            dict["infiltration"] = i[7]
            dict["webattack"] = i[8]
            dict["bruteforce"] = i[9]
            dict["dataset"] = i[10]
            arr.append(dict)
    return arr
if __name__ == "__main__":
    app.run()