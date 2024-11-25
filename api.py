import os
import uuid
from flask import Flask, request, render_template, Response, send_from_directory, jsonify

app = Flask(
    __name__, 
    template_folder="templates", 
    static_url_path="/", static_folder="static"
)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)