from flask import Flask, render_template, request, jsonify
from consultation import medical_consultation
from consultation import mental_consultation

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

if __name__ == '__main__':
    app.run(debug=True)