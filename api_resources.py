from flask_restful import Resource, reqparse
from flasgger import swag_from
from queries import *


class GroupsWithLimitedStudents(Resource):
    @swag_from('./docs/groups_with_limited_students.yml')
    def get(self, max_student_count):
        groups = find_groups_with_number_of_students(max_student_count)
        return [{'id': group.id, 'name': group.name} for group in groups]


class StudentsByCourseName(Resource):
    @swag_from('./docs/students_by_course_name.yml')
    def get(self, course_name):
        # Adjust the query to be case-insensitive
        students = find_students_by_course_name(course_name.lower())
        return [{'id': student.id, 'first_name': student.first_name,
                 'last_name': student.last_name} for student in students]


class AddStudent(Resource):
    @swag_from('./docs/add_student.yml')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'first_name',
            required=True,
            help="First name cannot be blank!")
        parser.add_argument(
            'last_name',
            required=True,
            help="Last name cannot be blank!")
        parser.add_argument('group_id', type=int)
        args = parser.parse_args()
        student_id = add_new_student(
            args['first_name'],
            args['last_name'],
            args.get('group_id'))
        return {
            'message': 'Student added successfully',
            'student_id': student_id}


class DeleteStudent(Resource):
    @swag_from('./docs/delete_student.yml')
    def delete(self, student_id):
        delete_student_by_id(student_id)
        return {'message': 'Student deleted successfully'}


class AssignStudentToCourse(Resource):
    @swag_from('./docs/assign_student_to_course.yml')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'student_id',
            required=True,
            type=int,
            help="Student ID cannot be blank!")
        parser.add_argument(
            'course_id',
            required=True,
            type=int,
            help="Course ID cannot be blank!")
        args = parser.parse_args()
        add_student_to_course(args['student_id'], args['course_id'])
        return {'message': 'Student assigned to course successfully'}


class RemoveStudentFromCourse(Resource):
    @swag_from('./docs/remove_student_from_course.yml')
    def delete(self, student_id, course_id):
        remove_student_from_course(student_id, course_id)
        return {'message': 'Student removed from course successfully'}
