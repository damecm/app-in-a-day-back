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

@app.route('/workout/add', methods=["POST"])
def add_workout():
    if request.content_type != 'application/json':
        return jsonify("Error: Data must be sent as JSON")

    post_data = request.get_json()
    name = post_data.get('name')
    demo_img = post_data.get('demo_img')
    category = post_data.get('category')

    if name == None:
        return jsonify('Error: Name is required')
    
    if category == None:
        return jsonify('Error: Category is required')

    new_workout = Workout(name, demo_img, category)
    db.session.add(new_workout)
    db.session.commit()

    return jsonify(workout_schema.dump(new_workout))


@app.route("/workout/get", methods=["GET"])
def get_workouts():
    all_workouts = Workout.query.all()
    result = many_workout_schema.dump(all_workouts)
    return jsonify(result)


@app.route("/workout/<id>", methods=["PUT"])
def workout_update(id):
    all_workouts = Workout.query.all(id)
    name = request.json['name']
    demo_img = request.json['demo_img']
    category = request.json['category']



@app.route('/workout/delete/<id>', methods=["DELETE"])
def delete_workout(id):
    delete_workout = db.session.query(Workout).filter(Workout.id == id).first()
    db.session.delete(delete_workout)
    db.session.commit()

    return jsonify('Workout Has Been Deleted')





if __name__ == '__main__':
    app.run(debug=True)


















