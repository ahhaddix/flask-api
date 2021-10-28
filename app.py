from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)


class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, idea):
        self.name = name
        self.idea = idea

class IdeaSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "idea")

idea_schema = IdeaSchema()
ideas_schema = IdeaSchema(many=True)


@app.route("/idea/add", methods=["POST"])
def add_idea():
    name = request.json.get("name")
    idea = request.json.get("idea")

    record = Idea(name, idea)
    db.session.add(record)
    db.session.commit()

    return jsonify(idea_schema.dump(record))

@app.route("/idea/get", methods=["GET"])
def get_all_ideas():
    all_ideas = Idea.query.all()
    return jsonify(ideas_schema.dump(all_ideas))


if __name__ == "__main__":
    app.run(debug=True)

