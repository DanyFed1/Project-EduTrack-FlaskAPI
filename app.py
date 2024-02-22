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
# api.add_resource(GroupsWithLimitedStudents, '/groups/<int:max_student_count>')
# api.add_resource(StudentsByCourseName, '/students/course/<string:course_name>')

# The below are tested in Insomnia/Postman
# api.add_resource(AddStudent, '/students/', methods=['POST', 'DELETE'])
# api.add_resource(
#     DeleteStudent,
#     '/students/delete/<int:student_id>',
#     methods=['DELETE'])
# api.add_resource(
#     AssignStudentToCourse,
#     '/student/assign_course',
#     methods=['POST'])
# api.add_resource(
#     RemoveStudentFromCourse,
#     '/student/remove_course/<int:student_id>/<int:course_id>',
#     methods=['DELETE'])

# More Restful Approach:
api.add_resource(GroupsResource, '/groups', '/groups/<int:group_id>', methods=['GET'])
api.add_resource(StudentResource, '/students', '/students/<int:student_id>')  # Handles adding and deleting students
api.add_resource(CourseResource, '/courses', '/courses/<int:course_id>')  # Existing courses resource
api.add_resource(CourseStudentsResource, '/courses/<string:course_name>/students')  # New resource for students by course name
api.add_resource(
    StudentCoursesResource,
    '/students/<int:student_id>/courses',
    '/students/<int:student_id>/courses/<int:course_id>')  # Adjusted for adding/removing courses


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the tables if they don't exist
        populate_empty_database()  # If tables are empty, populate with random data
    app.run(debug=True)
