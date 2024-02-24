from flask import Flask
from populate_empty_db import populate_empty_database
from api_resources import *
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger
from flask_cors import CORS

# Initialize app, api and Swagger
app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)
# Had to add as Insomnia stuggled with authentification sometimes without this
cors = CORS(app)


# Database. Default test user for a project is master_user with password: test_password_for_master_user
# db: fxmnd_task_10
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://master_user:test_password_for_master_user@localhost/fxmnd_task_10'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# More Restful Approach:
api.add_resource(
    GroupsResource,
    '/groups',
    '/groups/<int:group_id>',
    '/groups?max_student_count=<int:group_id>',
    methods=['GET'])
api.add_resource(
    StudentResource,
    '/students',
    '/students/<int:student_id>',
    methods=[
        'GET',
        'POST',
        'DELETE'])
api.add_resource(
    CourseResource,
    '/courses',
    '/courses/<int:course_id>',
    methods=['GET'])
api.add_resource(
    CourseStudentsResource,
    '/courses/students/<int:course_id>',
    methods=['GET'])
api.add_resource(
    StudentCoursesResource,
    '/students/<int:student_id>/courses',
    '/students/<int:student_id>/courses/<int:course_id>',
    methods=[
        'POST',
        'DELETE'])  # Adjusted for adding/removing courses


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the tables if they don't exist
        populate_empty_database()  # If tables are empty, populate with random data
    app.run(debug=True)
