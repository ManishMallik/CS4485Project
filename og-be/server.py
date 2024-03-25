from sqlalchemy import text
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
        model_type == "Tree Based"
    elif model_num == 3:
        model_type == "MST"
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
    with engine.connect() as conn:
        conn.execute(
            text(f"INSERT INTO Results (model, benign, dos, portscan, bot, infiltration, webattack, bruteforce, dataset) VALUES ({model_num}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {dataset_num})")
        )
        conn.commit()
    # step 4: return thr output to the front end
    return f"model_type = {model_type}\n dataset = {dataset}"
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