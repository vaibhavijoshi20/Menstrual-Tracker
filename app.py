from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

# Placeholder data for demonstration purposes
last_period_date = None  # You can set an actual date here

# Function to calculate the next period date based on the user's specific cycle length and last period date
def calculate_next_period_date(last_period_date, cycle_length):
    if last_period_date and cycle_length:
        last_date = datetime.strptime(last_period_date, '%Y-%m-%d')
        next_date = last_date + timedelta(days=cycle_length)
        return next_date.strftime('%Y-%m-%d')
    return None

# Function to calculate the estimated ovulation date based on the user's specific cycle length and last period date
def calculate_ovulation_date(last_period_date, cycle_length):
    if last_period_date and cycle_length:
        last_date = datetime.strptime(last_period_date, '%Y-%m-%d')
        ovulation_date = last_date + timedelta(days=(cycle_length // 2))
        return ovulation_date.strftime('%Y-%m-%d')
    return None

# Function to categorize mood based on ratings
def categorize_mood(mood_rating):
    if 1 <= mood_rating <= 4:
        return "Irritated"
    elif 5 <= mood_rating <= 7:
        return "Neutral"
    elif 8 <= mood_rating <= 10:
        return "Happy"
    else:
        return "Unknown"

@app.route('/', methods=['GET', 'POST'])
def period():
    global last_period_date  # Declare last_period_date as global
    if request.method == 'POST':
        last_period_date = request.form['last_period_date']
        cycle_length = int(request.form['cycle_length'])  # Retrieve cycle length from form

        # Calculate the next period date
        next_period_date = calculate_next_period_date(last_period_date, cycle_length)

        return redirect(url_for('period_result', date=next_period_date))
    return render_template('index.html')

@app.route('/ovulation', methods=['GET', 'POST'])
def ovulation():
    global last_period_date  # Declare last_period_date as global
    if request.method == 'POST':
        last_period_date = request.form['last_period_date']
        cycle_length = int(request.form['cycle_length'])  # Retrieve cycle length from form

        # Calculate the ovulation date
        ovulation_prediction = calculate_ovulation_date(last_period_date, cycle_length)

        return redirect(url_for('ovulation_result', date=ovulation_prediction))
    return render_template('ovulation.html')

@app.route('/mood', methods=['GET', 'POST'])
def mood():
    if request.method == 'POST':
        mood_rating = int(request.form['mood_rating'])
        
        # Categorize mood based on ratings
        mood_category = categorize_mood(mood_rating)
        
        return redirect(url_for('mood_result', mood=mood_category))
    return render_template('mood.html')

@app.route('/period_result/<date>')
def period_result(date):
    return render_template('period_result.html', next_period_date=date)

@app.route('/ovulation_result/<date>')
def ovulation_result(date):
    return render_template('ovulation_result.html', next_ovulation_date=date)

@app.route('/mood_result/<mood>')
def mood_result(mood):
    return render_template('mood_result.html', predicted_mood=mood)

if __name__ == '__main__':
    app.run(debug=True)
