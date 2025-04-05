from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
from scipy.stats import mode
from consultation import medical_consultation, mental_consultation
import pickle

app = Flask(__name__, static_folder='assets', static_url_path='/assets')
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/general.html', methods=['GET', 'POST'])
def general():
    if request.method == 'POST':
        age = request.form['age']
        gender = request.form['gender']
        query = request.form['query']
        
        response = medical_consultation(age, gender, query)
        return jsonify({'response': response})
    
    return render_template('general.html')


@app.route('/mental.html', methods=['GET', 'POST'])
def mental():
    if request.method == 'POST':
        age = request.form['age']
        gender = request.form['gender']
        stress_level = request.form['stressLevel']
        sleep_quality = request.form['sleepQuality']
        mood = request.form['mood']
        concern = request.form['concern']
        
        response = mental_consultation(age, gender, stress_level, sleep_quality, mood, concern)
        return jsonify({'response': response})
    
    return render_template('mental.html')


@app.route('/prediction.html')
def prediction():
    return render_template('prediction.html')

# Load models and label encoder
random_forest_model = joblib.load('random_forest_model.pkl')
naive_bayes_model = joblib.load('naive_bayes_model.pkl')
decision_tree_model = joblib.load('decision_tree_model.pkl')
le = joblib.load('label_encoder.pkl')

# Load all symptoms
all_symptoms = joblib.load('all_symptoms_list2.pkl')

def predict_disease(chosen_symptoms):
    input_vector = [1 if symptom in chosen_symptoms else 0 for symptom in all_symptoms]
    print(input_vector)
    rf_pred = random_forest_model.predict([input_vector])
    nb_pred = naive_bayes_model.predict([input_vector])
    dt_pred = decision_tree_model.predict([input_vector])
    
    predictions = np.array([rf_pred, nb_pred, dt_pred])
    majority_vote = mode(predictions, axis=0)[0].flatten()
    
    final_disease = le.inverse_transform(majority_vote)
    return final_disease[0]
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    symptoms = data.get('symptoms', [])

    prediction = predict_disease(symptoms)  # your disease_prediction.py logic
    return jsonify({'predicted_disease': prediction})


if __name__ == '__main__':
    app.run(debug=True)
