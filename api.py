from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    title = "home"
    owner = "Pablo"

    my_list = [1, 2, 3, 4, 5]

    return render_template("index.html", title=title, owner=owner, my_list=my_list)

@app.route("/page")
def page():
    my_list = [1, 2, 3, 4, 5]

    return render_template("page.html", my_list=my_list, some_text="test")

@app.route("/redirect-endpoint")
def redirect_endpoint():
    return redirect(url_for("page"))

@app.template_filter("reverse_string")
def reverse_string(s):
    return s[::-1]

@app.template_filter("repeat")
def reverse_string(s, times=1):
    return s*times

@app.route("/api/user", methods=["GET", "POST", "PUT"])
def user():
    users = [
        {
            "name": "Pablo",
            "age": 24
        },

        {
            "name": "Juan",
            "age": 22
        },
    ]

    if request.method == "GET":
        return users
    elif request.method == "POST":
        return "<h1>Create User</h1>"
    else:
        return "<h1>Errror</h1>", 400

@app.route("/api/greet/<name>")
def greet(name):
    return f"<h1>Hello {name}</h1>"

@app.route("/api/add/<number1>/<number2>")
def add(number1, number2):
    return f"{number1} + {number2} = {int(number1) + int(number2)}"

@app.route("/api/filter")
def filter():
    print(request.args)

    if "min" in request.args.keys():
        pass

    return str(request.args)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)