import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
from helpers.prediction import prediction
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

@app.route("/fcsv", methods=['POST'])
def fcsv():
    f = request.files.get('file')
    if not f:
        return jsonify({'result': 'Error', 'message': 'Input not found'})
    
    csvpath = os.path.join('usercontent', secure_filename(f.filename))
    f.save(csvpath)

    df = pd.read_csv(csvpath)
    for i in range(4):
        df['Inc_Time_Ch' + str(i)] = pd.to_timedelta(df['Inc_Time_Ch' + str(i)]).dt.seconds
    res = prediction(df)

    if(os.path.isfile(csvpath)):
        os.remove(csvpath)
    return jsonify(res)

@app.route("/fman", methods=['POST'])
def fman():
    feats = {}
    for i in range(4):
        feats['Mean_Ch' + str(i)] = request.form.get('Mean_Ch' + str(i))
    for i in range(4):
        feats['Inc_Time_Ch' + str(i)] = request.form.get('Inc_Time_Ch' + str(i))
    for i in range(4):
        feats['SE_Diff_Ch' + str(i)] = request.form.get('SE_Diff_Ch' + str(i))
    # terpaksa diulang 3 kali, katanya harus urut

    df = pd.DataFrame([feats])
    for i in range(4):
        df['Inc_Time_Ch' + str(i)] = pd.to_timedelta(df['Inc_Time_Ch' + str(i)]).dt.seconds
    res = prediction(df)

    return jsonify(res) 

@app.route("/rcsv", methods=['POST'])
def rcsv():
    f = request.files.get('file')
    if not f:
        return jsonify({'result': 'Error', 'message': 'Input not found'})
    
    csvpath = os.path.join('usercontent', secure_filename(f.filename))
    f.save(csvpath)

    df = pd.read_csv(csvpath)

    feats = {}

    for i in range(4):
        feats['Mean_Ch' + str(i)] =  df['Ch' + str(i)].mean()

    df['Time'] = pd.to_timedelta(df['Time'])
    for i in range(4):
        for j in range(1, len(df)):
            if (df['Ch' + str(i)].iloc[j] - df['Ch' + str(i)].iloc[0] > 2.2) or (j >= len(df) - 1):
                feats['Inc_Time_Ch' + str(i)] = (df['Time'].iloc[j] - df['Time'].iloc[0]).seconds
                break
    
    for i in range(4):
        feats['SE_Diff_Ch' + str(i)] = df['Ch' + str(i)].iloc[-1] - df['Ch' + str(i)].iloc[0]
    
    df = pd.DataFrame([feats])
    res = prediction(df)

    if(os.path.isfile(csvpath)):
        os.remove(csvpath)
    return jsonify(res) 

'''
@app.route("/rman", methods=['POST'])
def rman():
ga possible, yakali user disuruh masukin 4500 value
'''
if __name__ == '__main__':
    app.run(debug=True)