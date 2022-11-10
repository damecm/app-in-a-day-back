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



@app.route('/workout/get/<id>')
def get_one_workout(id):
    one_workout = db.session.query(Workout).filter(Workout.id == id).first()
    return jsonify(workout_schema.dump(one_workout))

@app.route('/workout/edit/<id>', methods=["PUT"])
def edit_workout(id):
    if request.content_type != 'application/json':
        return jsonify('Yo I told you it has to be JSON File')

    put_data = request.get_json()
    name = put_data.get('name')
    demo_img = put_data.get('demo_img')
    category = put_data.get('category')

    edit_workout = db.session.query(Workout).filter(Workout.id == id).first()
    if name != None:
        edit_workout.name = name
    if demo_img != None:
        edit_workout.demo_img = demo_img
    if category != None:
        edit_workout.category = category

    db.session.commit()

    return jsonify(workout_schema.dump(edit_workout))

@app.route('/workout/add/many', methods=['POST'])
def add_many_workout():
    if request.content_type != "application/json":
        return jsonify("YUck, please Make It a JSON File")

    post_data = request.get_json()
    workouts = post_data.get("workout")

    new_workouts = []

    for workout in workouts:
        name = workout.get('name')
        demo_img = workout.get('demo_img')
        category = workout.get('category')

        existing_workout_check = db.session.query(Workout).filter(Workout.name == name).first()
        if existing_workout_check is None:
            new_workout = Workout(name, demo_img, category)
            db.session.add(new_workout)
            db.session.commit()
            new_workouts.append(new_workout)

    return jsonify(many_workout_schema.dump(new_workouts))

if __name__ == '__main__':
    app.run(debug=True)

















