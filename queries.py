from models import db, Group, Student, Course, StudentCourses


def find_group_by_id(group_id):
    groups = Group.query.filter_by(id=group_id).first()
    return groups


def find_all_groups():
    groups = Group.query.all()
    return groups


def find_student_by_id(student_id):
    students = Student.query.filter_by(id=student_id).first()
    return students


def find_all_students():
    students = Student.query.all()
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


def find_course_by_id(course_id):
    return Course.query.filter_by(id=course_id).first()


def find_all_courses():
    return Course.query.all()


def add_student_to_courses(student_id, course_ids):
    for course_id in course_ids:
        if not StudentCourses.query.filter_by(
                student_id=student_id,
                course_id=course_id).first():
            student_course = StudentCourses(
                student_id=student_id, course_id=course_id)
            db.session.add(student_course)
    db.session.commit()


def remove_student_from_course(student_id, course_id):
    StudentCourses.query.filter_by(
        student_id=student_id,
        course_id=course_id).delete()
    db.session.commit()


def remove_student_from_all_courses(student_id):
    StudentCourses.query.filter_by(student_id=student_id).delete()
    db.session.commit()


def find_students_by_course_name(course_name):
    """Find all students related to a course by its name."""
    return Student.query \
        .join(StudentCourses) \
        .join(Course) \
        .filter(Course.name.ilike(course_name)) \
        .all()


def find_groups_with_max_or_less_students(max_student_count):
    groups = db.session.query(
        Group.id,
        Group.name,
        db.func.count(Student.id).label('student_count')
    ).join(Student, isouter=True).group_by(Group.id).having(
        db.func.count(Student.id) <= max_student_count
    ).all()
    return [
        {'id': group.id, 'name': group.name, 'student_count': group.student_count}
        for group in groups
    ]
