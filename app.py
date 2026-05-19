from flask import Flask, render_template, request, session
import time

app = Flask(__name__)
app.secret_key = "graysentinel_secret"

# Read logs from file
with open('logs/auth.log', 'r') as file:
    LOG_DATA = file.read()

CORRECT_IP = "185.220.101.34"

@app.route('/')
def home():

    if 'attempts' not in session:
        session['attempts'] = 0

    if 'score' not in session:
        session['score'] = 100

    if 'start_time' not in session:
        session['start_time'] = time.time()

    return render_template(
        'challenge.html',
        logs=LOG_DATA,
        attempts=session['attempts'],
        score=session['score']
    )

@app.route('/submit', methods=['POST'])
def submit():

    ip = request.form['ip']
    user = request.form['user']
    attack = request.form['attack']

    if not ip or not user or not attack:
        return "Please fill all fields"

    elapsed_time = int(time.time() - session['start_time'])

    if (
        ip == "185.220.101.34"
        and user == "developer"
        and attack.lower() == "ssh brute force"
    ):

        result = "Excellent investigation!"
        success = True

    else:

        session['attempts'] += 1
        session['score'] -= 10

        result = "Some answers are incorrect."
        success = False

    hint = None

    if session['attempts'] >= 2:
        hint = "Hint: Look for repeated failed SSH logins from the same IP."

    return render_template(
        'result.html',
        result=result,
        success=success,
        attempts=session['attempts'],
        score=session['score'],
        elapsed_time=elapsed_time,
        hint=hint
    )

if __name__ == '__main__':
    app.run(debug=True)
