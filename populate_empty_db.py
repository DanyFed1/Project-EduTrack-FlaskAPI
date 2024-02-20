import random
from models import db, Group, Student, Course, StudentCourses


def generate_random_groups_and_add_them_to_db(n=10):
    for i in range(n):
        name = f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}-{random.randint(10, 99)}"
        group = Group(name=name)
        db.session.add(group)
    db.session.commit()


def create_courses_and_add_them_to_db():
    course_names = [
        "Math",
        "Biology",
        "History",
        "English",
        "Physics",
        "Chemistry",
        "Geography",
        "Art",
        "Music",
        "Physical Education"]
    for name in course_names:
        course = Course(name=name, description=f"{name} Course Description")
        db.session.add(course)
    db.session.commit()


def generate_random_students_and_add_them_to_db(n=200):
    first_names = [
        "John",
        "Jane",
        "Mike",
        "Sara",
        "Laura",
        "Chris",
        "Robert",
        "Daniel",
        "Emma",
        "Olivia",
        "Noah",
        "Liam",
        "Sophia",
        "Mia",
        "Charlotte",
        "Amelia",
        "Evelyn",
        "Abigail",
        "Harper",
        "Emily"]
    last_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Brown",
        "Jones",
        "Miller",
        "Davis",
        "Garcia",
        "Rodriguez",
        "Wilson",
        "Martinez",
        "Anderson",
        "Taylor",
        "Thomas",
        "Hernandez",
        "Moore",
        "Martin",
        "Jackson",
        "Thompson",
        "White"]
    for i in range(n):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        student = Student(first_name=first_name, last_name=last_name)
        db.session.add(student)
    db.session.commit()


def assign_random_students_to_groups():
    students = Student.query.all()
    groups = Group.query.all()
    for student in students:
        # Adding None to simulate the chance of not being assigned
        group = random.choice(groups + [None] * 10)
        if group:
            student.group_id = group.id
    db.session.commit()


def assign_courses_to_random_students():
    students = Student.query.all()
    courses = Course.query.all()
    for student in students:
        assigned_courses = random.sample(courses, random.randint(1, 3))
        for course in assigned_courses:
            student_course = StudentCourses(
                student_id=student.id, course_id=course.id)
            db.session.add(student_course)
    db.session.commit()


def tables_are_empty():
    """We do not want to populate db unless all tables are empty"""
    return not Group.query.first() and not Student.query.first() and not Course.query.first()


def populate_empty_database():
    if tables_are_empty():
        generate_random_groups_and_add_them_to_db()
        create_courses_and_add_them_to_db()
        generate_random_students_and_add_them_to_db()
        assign_random_students_to_groups()
        assign_courses_to_random_students()
        print("Database populated successfully.")
    else:
        print("Database is not empty.")
