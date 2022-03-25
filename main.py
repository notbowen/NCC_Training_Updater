from flask import Flask, render_template, request, jsonify, make_response
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/api/get_data', methods=['GET'])
def get_data():
    with open("training_data.json", "r")as f:
        data = json.load(f)
        f.close()

    response = jsonify(data)
    # So that google sites can somehow get the data, without this it somehow doesn't work
    # idk why
    response.headers.add("Access-Control-Allow-Origin", "*")

    return make_response(response, 200)

@app.route('/api/update_data', methods=['POST'])
def update_data():
    attire = request.form['attire']
    venue = request.form['venue']
    timing = request.form['timing']

    # Input formatting
    if attire == "": attire = "Empty Value Received"
    if venue == "": venue = "Empty Value Received"
    if timing == "": timing = "Empty Value Received"

    data = {
        "attire": attire,
        "venue": venue,
        "time": timing
    }

    with open("training_data.json", "w") as f:
        json.dump(data, f, indent=4)
        f.close()

    return render_template("updated.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
