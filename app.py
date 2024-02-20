from flask import Flask
from populate_empty_db import populate_empty_database
from api_resources import *
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger

# Initialize app, api and Swagger
app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

# Database. Default test user for a project is master_user with password: test_password_for_master_user
#db: fxmnd_task_10
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://master_user:test_password_for_master_user@localhost/fxmnd_task_10'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register resources
api.add_resource(GroupsWithLimitedStudents, '/groups/<int:max_student_count>')
api.add_resource(StudentsByCourseName, '/students/course/<string:course_name>')

# The below are tested in Insomnia/Postman
api.add_resource(AddStudent, '/student/add', methods=['POST'])
api.add_resource(
    DeleteStudent,
    '/student/delete/<int:student_id>',
    methods=['DELETE'])
api.add_resource(
    AssignStudentToCourse,
    '/student/assign_course',
    methods=['POST'])
api.add_resource(
    RemoveStudentFromCourse,
    '/student/remove_course/<int:student_id>/<int:course_id>',
    methods=['DELETE'])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the tables if they don't exist
        populate_empty_database()  # If tables are empty, populate with random data
    app.run(debug=True)
