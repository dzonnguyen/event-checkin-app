from flask import Flask, request
import datetime

app = Flask(__name__)

# Store check-ins
checkins = []

@app.route('/')
def home():
    return "<h1>Welcome to Event Check-in!</h1>"

# The endpoint that will be triggered by scanning QR
@app.route('/checkin')
def checkin():
    participant_id = request.args.get('id')
    timestamp = datetime.datetime.now()
    if participant_id:
        checkins.append((participant_id, timestamp))
        return f"<h2>Check-in successful for ID: {participant_id} at {timestamp}</h2>"
    else:
        return "<h2>Invalid check-in. No ID provided.</h2>"

# See who has checked in
@app.route('/checkins')
def show_checkins():
    html = "<h1>Checked-in Participants</h1><ul>"
    for pid, time in checkins:
        html += f"<li>{pid} - {time}</li>"
    html += "</ul>"
    return html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
