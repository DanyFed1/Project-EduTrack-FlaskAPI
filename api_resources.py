from flask_restful import Resource, reqparse
from flask import request
from flasgger import swag_from
from queries import *


class GroupsResource(Resource):
    @swag_from('./docs/groups_operations.yml')
    def get(self, group_id=None):
        max_student_count = request.args.get(
            'max_student_count', default=None, type=int)

        # If a group_id is provided, find and return the specific gorup
        if group_id:
            group = find_group_by_id(group_id)
            return [{'id': group.id, 'name': group.name}]

        # if ?max_student_count= provided
        if max_student_count is not None:
            groups = find_groups_with_max_or_less_students(max_student_count)
        else:
            groups = find_all_groups()

        # Format the output
        return [{'id': group.id, 'name': group.name, 'student_count': getattr(
            group, 'student_count', None)} for group in groups]


class StudentResource(Resource):
    @swag_from('./docs/student_operations.yml')
    def get(self, student_id=None):
        if student_id:
            student = find_student_by_id(student_id)
            return [{'id': student.id,
                     'name': student.first_name,
                     'surname': student.last_name}]
        else:
            students = find_all_students()
            return [{'id': student.id, 'name': student.first_name,
                     'surname': student.last_name} for student in students]

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

    def delete(self, student_id):
        delete_student_by_id(student_id)
        return {'message': 'Student deleted successfully'}


class CourseResource(Resource):
    @swag_from('./docs/course_operations.yml')
    def get(self, course_id=None):
        if course_id:
            course = find_course_by_id(course_id)
            return [{'id': course.id, 'name': course.name,
                     'description': course.description}]
        else:
            courses = find_all_courses()
            return [{'id': course.id, 'name': course.name,
                     'description': course.description} for course in courses]


class CourseStudentsResource(Resource):
    @swag_from('./docs/course_students_operations.yml')
    def get(self, course_id):
        """Find all students related to the course with a given course_id."""
        students = find_students_by_course_id(course_id)
        return [{'id': student.id, 'first_name': student.first_name,
                 'last_name': student.last_name} for student in students]


class StudentCoursesResource(Resource):
    @swag_from('./docs/student_course_operations.yml')
    def post(self, student_id):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'course_id',
            action='append',
            required=True,
            help="Course ID(s) cannot be blank!")
        args = parser.parse_args()
        add_student_to_courses(student_id, args['course_id'])
        return {'message': 'Students assigned to course successfully'}

    def delete(self, student_id, course_id):
        """Remove a student from one of his or her courses."""
        remove_student_from_course(student_id, course_id)
        return {'message': 'Student removed from course successfully'}
