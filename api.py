import os
import uuid
from flask import Flask, request, render_template, Response, send_from_directory, jsonify
import pandas as pd

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", error=False)
    elif request.method == "POST":    
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "pablo" and password == "pablo":
            return "Success"
        else:
            return render_template("index.html", error=True)

@app.route("/upload-file", methods=["POST"])
def upload_file():
    file = request.files["file"]

    if file.content_type == "text/plain":
        return file.read().decode()
    elif (
        file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or
        file.content_type == ", application/vnd.ms-excel"
    ):
        df = pd.read_excel(file)
        return df.to_html()

@app.post("/convert-csv")
def convert_csv():
    file = request.files["file"]

    df = pd.read_excel(file)
    
    response = Response(df.to_csv(), mimetype="text/csv", headers={
        "Content-Disposition": "attachment; filename=result.csv"
    })

    return response

@app.post("/convert-csv2")
def convert_csv_2():
    file = request.files["file"]
    
    df = pd.read_excel(file)

    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    
    filename = f"{uuid.uuid4()}.csv"

    df.to_csv(os.path.join("downloads", filename))

    return render_template("download.html", filename=filename)

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory("downloads", filename, download_name="result")

@app.post("/handle-post")
def handle_post():
    greeting = request.json["greeting"]
    name = request.json["name"]

    with open("file.txt", "w") as f:
        f.write(f"{greeting} {name}")
    
    return {
        "message": "Written!"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)