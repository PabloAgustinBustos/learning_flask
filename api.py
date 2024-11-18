from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:postgres@localhost:5432/pythondb"

db = SQLAlchemy(app)

api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)

    def __repr__(self):
        return f"User(name = {self.name}, email = {self.email})"

user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str, required=True, help="Name cannot be blank")
user_args.add_argument("email", type=str, required=True, help="Email cannot be blank")

# Response's body structure
userFields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String
}

# Router de users
class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users

    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"])

        db.session.add(user)

# Bindea la ruta al router
api.add_resource(Users, "/api/users/")

@app.route("/")
def home():
    return "<h1>Flask REST API</h1>"

@app.route("/greet/<name>")
def greet(name):
    return f"<h1>Hello {name}</h1>"

@app.route("/add/<number1>/<number2>")
def add(number1, number2):
    return f"{number1} + {number2} = {int(number1) + int(number2)}"

@app.route("/filter")
def filter():
    return str(request.args)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)