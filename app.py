from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

baseddir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseddir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Workout(db.Model): 
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    demo_img = db.Column(db.String, unique=True)
    category = db.Column(db.String, unique=True)

    def __init__(self, name, demo_img, category):
        self.name = name
        self.demo_img = demo_img
        self.category = category

class WorkoutSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'demo_img', 'category')


workout_schema = WorkoutSchema()
many_workout_schema = WorkoutSchema(many=True)



app.route('movie/edit')


@app.route("/workouts/get", methods=["GET"])
def get_workouts():
    all_workouts = Workout.query.all()
    result = many_workout_schema.dump(all_workouts)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

















