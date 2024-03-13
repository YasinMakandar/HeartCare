# Import libraries
import re
import numpy as np
from flask import Flask, request, jsonify, render_template,redirect
import pickle
import math as math

app = Flask(__name__)

# Load the model
# lr_model = pickle.load(open('models.pkl', 'rb'))
# rf_classifier = pickle.load(open('models.pkl', 'rb'))

all_models=pickle.load(open('models.pkl', 'rb'))
all_models2=pickle.load(open('models.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def hey():
    return render_template("signin.html")
@app.route('/index', methods=['GET', 'POST'])
def hello():
    return render_template("index.html")
@app.route('/heart', methods=['GET', 'POST'])
def heart():
    return render_template("heart.html")
@app.route('/chatu',methods=['GET', 'POST'])
def chatu():
    return render_template('chatu.html')
@app.route('/accordion__content', methods=['GET', 'POST'])
def accordion__content():
    return render_template("index.html")
@app.route('/login', methods=['POST'])
def login():
    # Extract email and password from the request JSON data
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Perform authentication logic (example)
    # You should replace this with your actual authentication logic
    if email == email and password == password:
        # If authentication succeeds, redirect to index.html
        return jsonify({'redirect': '/index'})
    else:
        # If authentication fails, return an error response
        return jsonify({'error': 'Invalid email or password'}), 401
# @app.route('/submitform', methods = ['POST'])
# def submitform():
#     name = request.form['name']
#     email= request.form['email']
#     age=request.form['age']
#     sex=request.form['gender']
#     cp=request.form['cp']
#     trestbps=request.form['trestbps']
#     chol=request.form['chol']
#     fbs=request.form['fbs']
#     restecg=request.form['restecg']
#     thalach=request.form['thalach']
#     exang=request.form['exang']
#     oldpeak=request.form['oldpeak']
#     thal=request.form['thal']
#     print("The email address is '" + age + "|"+sex)
#     # return redirect('/api/{age}/{sex}/{cp}/{trestbps}/{chol}/{fbs}/{restecg}/${thalach}/${exang}/${oldpeak}/${thal}')
#     return redirect()
    
@app.route('/api', methods=['GET', 'POST'])
@app.route('/api', methods=['GET', 'POST'])
def predict():
    name = request.form['name']
    email= request.form['email']
    age=request.form['age']
    fgender=request.form['gender']
    cp=request.form['cp']
    trestbps=request.form['trestbps']
    chol=request.form['chol']
    fbs=request.form['fbs']
    restecg=request.form['restecg']
    thalach=request.form['thalach']
    exang=request.form['exang']
    oldpeak=request.form['oldpeak']
    slope=request.form['slope']
    ca=request.form['ca']
    thal=request.form['thal']
    if trestbps=='':
        trestbps=95
    if chol=='':
        chol=150
    if thalach=='':
        thalach=72
    if oldpeak=='':
        oldpeak=2

    recieved_features=[age, fgender, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak,slope,ca,thal]
    input_data={}
    input_data["age"]=age
    input_data["Gender"]=fgender
    input_data["Chest Pain Types"]=cp
    input_data["Resting Blood Pressure(in mm/Hg)"]=trestbps
    input_data["Cholesterol Level"]=chol
    input_data["is Fasting Blood Pressure>120mg/Dl?"]=fbs
    input_data["Resting Electro Cardio Graphic Result"]=restecg
    input_data["Maximum Heart Rate Achieved"]=thalach
    input_data["Does Exercise Induced Angina?"]=exang
    input_data["Old Peak (ST Depression Induced by Exercise Relative to Rest)"]=oldpeak
    input_data["Slope of ST Segment"]=slope
    input_data["number of major vessels (0-3) colored by flourosopy"]=ca
    input_data["Thal Type"]=thal

    if fgender=="Male":
        gender=1
    else:
        gender=0
    
    if thal=="Normal":
        thal=0
    elif thal=="Fixed Defect":
        thal=1
    else:
        thal=2

    if restecg=="Normal":
        restecg=0
    elif restecg=="STT Abnormality":
        restecg=1
    else:
        restecg=2
    if exang=="Yes":
        exang=1
    else:
        exang=0

    age=int(age)
    cp=int(cp)
    trestbps=int(trestbps)
    chol=int(chol)
    fbs=int(fbs)
    thalach=int(thalach)
    oldpeak=int(oldpeak)
    slope=int(slope)
    ca=int(ca)
    features=[age, gender, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak,slope,ca,thal]
    
    dict_results = {}
    avg_prediction = 0
    for model in all_models:
        prediction = model.predict([features])[0]
        avg_prediction += prediction

    avg_prediction /= len(all_models)  # Calculate the average prediction
    avg_prediction = min(avg_prediction, 1)  # Limit to a maximum of 1 (representing 100%)
    heart_disease_likelihood = avg_prediction * 100  # Convert to percentage

    
    # avg_prediction = 0
    # for model in all_models:
    #     prediction = model.predict([features])[0]
    #     avg_prediction += prediction
    # avg_prediction /= len(all_models)
    #  # Convert the average prediction to a percentage representing the likelihood of having heart disease
    # heart_disease_likelihood = min(avg_prediction * 100, 100)  # Limit to 100%
    
    # avg = 0

    # for model in all_models:
    #     print("Model:", model)
    #     res = model.predict([features])[0]  # Extracting the single prediction from the numpy array
    #     print("res:", res)
    #     if res == 1:
    #         dict_results[model] = "High Chance of Heart Disease"
    #     else:
    #         dict_results[model] = "Low Chance of Heart Disease"
    #     avg += res

    # accuracy = avg / len(all_models)  # Divide by the number of models, not a fixed number
    # accuracy = min(accuracy * 100, 100)  # Convert accuracy to percentage

    personal_info=[name,email]
    responses=[input_data, dict_results, personal_info, hear_disease_likelihood]
    
    return render_template("result.html", result=responses)

    


    
if __name__ == '__main__':
    app.run(port=5500, debug=True)


    
