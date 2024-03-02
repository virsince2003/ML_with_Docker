from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import pickle
from joblib import dump, load

app = Flask(__name__)

# loading the model for prediction
with open("classifier.pkl", "rb") as model_file:
    prediction = pickle.load(model_file)

@app.route("/")
def homepage():
    return "Welcome to the web application"

@app.route("/predict", methods=["GET"])
def bank_note_authenticator():
    try:
        variance = float(request.args.get("variance", default=0))
        skewness = float(request.args.get("skewness", default=0))
        curtosis = float(request.args.get("curtosis", default=0))
        entropy = float(request.args.get("entropy", default=0))
        
    
        prediction_result = prediction.predict([[variance, skewness, curtosis, entropy]])
        
        return "The possible answer is " + str(prediction_result)
    except ValueError:
        return "Invalid input format"
 
    
@app.route("/test",methods=["POST"])
def test_data():
    try:
        if "file" not in request.files:
            return "No file uploaded", 400
        
        df_test = pd.read_csv(request.files.get("file"))
        df_test.head(2)
        test_prediction = prediction.predict(df_test)
        return "Predictions are " + str(list(test_prediction)), 200

    except Exception as e:
        return str(e), 500



if __name__ == "__main__":
    app.run(debug=True)