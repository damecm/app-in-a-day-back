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


@app.route('/workout/get/<id>')
def get_one_workout(id):
    one_workout = db.session.query(Workout).filter(Workout.id == id).first()
    return jsonify(workout_schema.dump(one_workout))



#@app.route("/workout/<id>", methods=["PUT"])
#def workout_update(id):
#    all_workouts = Workout.query.all(id)
#    name = request.json['name']
#    demo_img = request.json['demo_img']
#    category = request.json['category']



@app.route('/workout/delete/<id>', methods=["DELETE"])
def delete_workout(id):
    delete_workout = db.session.query(Workout).filter(Workout.id == id).first()
    db.session.delete(delete_workout)
    db.session.commit()

    return jsonify('Workout Has Been Deleted')





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













{
    "name": "sit ups",
    "category": "core",
    "demo_img": "https://i.imgur.com/4778qbz.png"
},
{
    "name": "plank",
    "category": "core",
    "demo_img": "https://i.imgur.com/k1bvaTr.png"
},
{
    "name": "side to side",
    "category": "core",
    "demo_img": "https://i.imgur.com/LTO4vop.png"
},
{
    "name": "flutter kicks",
    "category": "core",
    "demo_img": "https://i.imgur.com/DBxG2O3.png"
},
{
    "name": " swimmers",
    "category": "core",
    "demo_img": "https://i.imgur.com/LMFTGTn.png"
},
{
    "name": "bicycle kicks",
    "category": "core",
    "demo_img": "image.png"
},






