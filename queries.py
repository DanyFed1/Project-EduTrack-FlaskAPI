from models import db, Group, Student, Course, StudentCourses


def find_groups_with_number_of_students(max_student_count):
    groups = Group.query.join(
        Student,
        Group.id == Student.group_id,
        isouter=True) .group_by(
        Group.id) .having(
            db.func.count(
                Student.id) <= max_student_count) .all()
    return groups


def find_students_by_course_name(course_name):
    students = Student.query.join(StudentCourses).join(
        Course).filter(Course.name.ilike(course_name)).all()
    return students


def add_new_student(first_name, last_name, group_id=None):
    new_student = Student(
        first_name=first_name,
        last_name=last_name,
        group_id=group_id)
    db.session.add(new_student)
    db.session.commit()
    return new_student.id


def delete_student_by_id(student_id):
    Student.query.filter_by(id=student_id).delete()
    db.session.commit()


def add_student_to_course(student_id, course_id):
    student_course = StudentCourses(student_id=student_id, course_id=course_id)
    db.session.add(student_course)
    db.session.commit()


def remove_student_from_course(student_id, course_id):
    StudentCourses.query.filter_by(
        student_id=student_id,
        course_id=course_id).delete()
    db.session.commit()
