import joblib
import os

def prediction(dataframe):
    modelpath = os.path.join("model", "ulcer_svm.pkl")
    with open(modelpath, 'rb') as f:
        model = joblib.load(f)
    
    result = model.predict(dataframe)
    return {"Prediction": str(result[0])}
