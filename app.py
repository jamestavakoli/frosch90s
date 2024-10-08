from flask import Flask, render_template, redirect, url_for, session, jsonify, request
from flask_session import Session  # Correct import for Flask-Session
from datetime import datetime, timedelta


TIMEOUT_DURATION_IN_MINUTES = 8

app = Flask(__name__)
app.secret_key = 'berlinfrogs'  # Replace with your secret key for sessions

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def is_out_of_time():
      # If session doesn't have start time, set it
    if 'start_time' not in session:
        session['start_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get the current time and the stored start time
    start_time = datetime.strptime(session['start_time'], '%Y-%m-%d %H:%M:%S')
    current_time = datetime.now()

    # Calculate the elapsed time
    elapsed_time = current_time - start_time
    if elapsed_time > timedelta(minutes=TIMEOUT_DURATION_IN_MINUTES):
        return True
    return False


@app.route('/')
def home():
    if is_out_of_time():
        return redirect(url_for('timeout'))

    get_frog_info_from_session()
    return render_template('index.html', frog_info=get_frog_info_from_session())


@app.route('/timeout')
def timeout():
    return render_template('timeout.html')

@app.route('/login')
def login():
    return render_template('login.html')    

@app.route('/register')
def register():
    return render_template('registration.html')

@app.route('/reset')
def reset():
    # Reset the timer
    session.pop('start_time', None)  # Remove the start time from the session

    # remove frog info
    session.pop('frog_name', None)
    session.pop('frog_arms', None)
    session.pop('first_name', None)
    session.pop('last_name', None)

    return redirect(url_for('home'))

@app.route('/submit_frog_info', methods=['POST'])
def submit_frog_info():
    data = request.json  # Retrieve the JSON data sent from the client

    # Store the frog's information in the session
    session['first_name'] = data.get('first_name')
    session['last_name'] = data.get('last_name')
    session['frog_name'] = data.get('frog_name')
    session['frog_arms'] = data.get('frog_arms')

    # print out the frog information for debugging
    print(get_frog_info_from_session())

    # Return a success response
    return jsonify({'success': True})

def get_frog_info_from_session():
    # Retrieve frog information from the session
    return {
        'first_name': session.get('first_name'),
        'last_name': session.get('last_name'),
        'frog_name': session.get('frog_name'),
        'frog_arms': session.get('frog_arms')
    }


if __name__ == '__main__':
    app.run(debug=True)
