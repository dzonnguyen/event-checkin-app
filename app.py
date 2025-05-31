from flask import Flask, request, render_template, session, redirect, url_for
import datetime
import pandas as pd

app = Flask(__name__)
app.secret_key = 'TuMeu-3010'
app.permanent_session_lifetime = timedelta(hours=1)

APP_PW = 'vietx2025'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == APP_PW:
            session.permanent = True
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Store check-ins
checkins = []

p_data = pd.read_csv('participants.csv')
p_data['id'] = p_data['id'].astype(str)
p_data['checked_in'] = 'no'

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/check_guest_info', methods=['GET', 'POST'])
@login_required
def check_guest_info():
    if request.method == 'POST':
        user_input = request.form['my_input']  # Get the value from the form
        temp = p_data[p_data['id'] == user_input]
        if not temp.empty:        
            p_name = temp['name'].iloc[0]
            p_email = temp['email'].iloc[0]
            p_telephone = temp['mobile'].iloc[0]
            p_job = temp['job'].iloc[0]
            p_interest = temp['topics'].iloc[0]
            p_question = temp['questions'].iloc[0]
            p_checkin = temp['checked_in'].iloc[0]
            html =  f"<h2>Guest information for ID: {user_input}</h2> \
            <p>Name: <b>{p_name}</b> </p> \
            <p>Telephone: <b>{p_telephone}</b> </p> \
            <p>Email: <b>{p_email}</b> </p> \
            <p>Job: <b>{p_job}</b> </p> \
            <p>Interest: <b>{p_interest}</b> </p> \
            <p>Question: <b>{p_question}</b> </p> \
            <p>Checked-In?: <b>{p_checkin}</b> </p>"
            return html
        else:
            return "<h2>Invalid check-in. Invalid ID.</h2>"  
    return render_template('check_guest.html')    

# The endpoint that will be triggered by scanning QR
@app.route('/checkin')
@login_required
def checkin():
    participant_id = request.args.get('id')
    temp = p_data[p_data['id'] == participant_id]
    if not temp.empty:
        p_name = temp['name'].iloc[0]
        p_email = temp['email'].iloc[0]
        p_telephone = temp['mobile'].iloc[0]
        p_job = temp['job'].iloc[0]
        p_interest = temp['topics'].iloc[0]
        p_question = temp['questions'].iloc[0]
        timestamp = datetime.datetime.now()
        checkins.append((participant_id, timestamp))
        p_data.loc[p_data['id'] == participant_id, 'checked_in'] = 'yes'
        html =  f"<h2>Check-in successful for ID: {participant_id} at {timestamp}</h2> \
        <p>Name: <b>{p_name}</b> </p> \
        <p>Telephone: <b>{p_telephone}</b> </p> \
        <p>Email: <b>{p_email}</b> </p> \
        <p>Job: <b>{p_job}</b> </p> \
        <p>Interest: <b>{p_interest}</b> </p> \
        <p>Question: <b>{p_question}</b> </p>" 
        return html
    else:
        return "<h2>Invalid check-in. Invalid ID.</h2>"
    

# See who has checked in
@app.route('/show_checkins')
@login_required
def show_checkins():
    temp = p_data[p_data['checked_in'] == 'yes']
    temp = temp[['id','name','email','mobile']]
    html = temp.to_html(classes = 'styled-table', index = False, justify = 'center') 
    return render_template('show_checkins.html', table_html = html)

@app.route('/show_not_there')
@login_required
def show_not_there():
    temp = p_data[p_data['checked_in'] == 'no']
    temp = temp[['id','name','email','mobile']]
    html = temp.to_html(classes = 'styled-table', index = False, justify = 'center') 
    return render_template('show_checkins.html', table_html = html)

@app.route('/questions')
@login_required
def questions():
    temp = p_data[p_data['questions'].notnull()]
    temp = temp[['id','name','questions']]
    html = temp.to_html(classes = 'styled-table', index = False, justify = 'center') 
    return render_template('show_checkins.html', table_html = html)

@app.route('/manual_checkin', methods=['GET', 'POST'])
@login_required
def manual_checkin():
    if request.method == 'POST':
        user_input = request.form['my_input']  # Get the value from the form
        temp = p_data[p_data['id'] == user_input]
        if not temp.empty:        
            p_name = temp['name'].iloc[0]
            p_email = temp['email'].iloc[0]
            p_telephone = temp['mobile'].iloc[0]
            p_job = temp['job'].iloc[0]
            p_interest = temp['topics'].iloc[0]
            p_question = temp['questions'].iloc[0]
            timestamp = datetime.datetime.now()
            checkins.append((user_input, timestamp))
            p_data.loc[p_data['id'] == user_input, 'checked_in'] = 'yes'
            html =  f"<h2>Check-in successful for ID: {user_input} at {timestamp}</h2> \
            <p>Name: <b>{p_name}</b> </p> \
            <p>Telephone: <b>{p_telephone}</b> </p> \
            <p>Email: <b>{p_email}</b> </p> \
            <p>Job: <b>{p_job}</b> </p> \
            <p>Interest: <b>{p_interest}</b> </p> \
            <p>Question: <b>{p_question}</b> </p>" 
            return html
        else:
            return "<h2>Invalid check-in. Invalid ID.</h2>"  
    return render_template('manual_check-in.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
