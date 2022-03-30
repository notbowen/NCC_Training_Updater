from flask import Flask, render_template, request, jsonify, make_response
from werkzeug.utils import secure_filename

import json
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/api/get_data', methods=['GET'])
def get_data():
    with open("training_data.json", "r") as f:
        data = json.load(f)
        f.close()

    response = jsonify(data)
    # So that google sites can somehow get the data, without this it somehow doesn't work
    # idk why
    response.headers.add("Access-Control-Allow-Origin", "*")

    return make_response(response, 200)


@app.route('/api/update_data', methods=['POST'])
def update_data():
    if request.method == "POST":
        # Get values
        attire = request.form['attire']
        venue = request.form['venue']
        timing = request.form['timing']
        date = request.form['date'] # Date in form of yyyy-mm-dd

        timetable = request.files['timetable']
        fname = secure_filename(timetable.filename)

        # Parse Date
        dateParsed = date.split("-")
        dateParsed = dateParsed[2] + "/" + dateParsed[1] + "/" + dateParsed[0][2:]

        # Dump values into dict
        data = {
            "attire": attire,
            "venue": venue,
            "time": timing,
            "date": dateParsed,
            "imgSrc": "https://ncctrainingupdater.hubowen.repl.co/static/images/" + str(fname)
        }

        # Update values
        with open("training_data.json", "w") as f:
            json.dump(data, f, indent=4)
            f.close()

        # Get persistent data
        # prevImage: used to delete former image
        with open("persistent_data.json", "r") as f:
            persistent_data = json.load(f)
            f.close()

        # Get prevImg and delete
        prevImg = persistent_data["prevImage"]
        try:
            os.remove(os.path.join(app.root_path, 'static', 'images', prevImg))
        except:
            print("[ERROR] Couldn't delete file!")
            
        # Save image
        try:
            timetable.save(os.path.join(app.root_path, 'static', 'images',  fname))
        except Exception as e:
            return render_template("errorUpload.html", errorLog=e)

        # Update prevImg to current and save
        persistent_data["prevImage"] = fname
        with open("persistent_data.json", "w") as f:
            json.dump(persistent_data, f, indent=4)

        # return successfully updated
        return render_template("updated.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
