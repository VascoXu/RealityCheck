import os
import json
import csv
from flask import Flask, render_template, request, session, redirect, url_for, make_response ,jsonify

app = Flask(__name__)
app.secret_key = 'test'


@app.route('/')
def home():
    """Render home page"""
    return render_template('index.html')

@app.route('/phrases', methods=['GET'])
def phrases():
    try:
        with open('phrases.txt', 'r') as file:
            phrases = file.read()
        response = make_response(phrases)
        response.headers['Content-Type'] = 'text/plain'
        return response
    except FileNotFoundError:
        return make_response("File not found", 404)

@app.route('/submit', methods=['POST'])
def submit():
    session['participant_id'] = request.form['participant-id']
    session['session_id'] = request.form['session-id']
    session['keyboard_type'] = request.form['keyboard-type']
    session['uid'] = request.form['uid']
    return redirect(url_for('/main'))


@app.route('/download', methods=['POST'])
def download():
    # retrieve data from Javascript
    data = request.get_json()
    filename = data['filename']
    json_content = data['json_data']
    csv_content = data['csv_data']

    # create directory, if not exists
    base_dir = os.path.join('data', filename)
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # save data
    base_name = os.path.join(base_dir, filename)
    if data is None:
        return jsonify({"error": "No JSON data received"}), 400
    try:
        # save JSON
        with open(f'{base_name}.json', 'w') as f:
            json.dump(json_content, f)

        # save CSV
        with open(f'{base_name}.csv', 'w') as f:
            f.write(csv_content)

        return jsonify({"success": True}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route('/main', methods=['GET', 'POST'])
def main():
    """Render main page"""
    if request.method == 'GET':
        return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
