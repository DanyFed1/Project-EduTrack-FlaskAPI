from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    students = db.relationship('Student', backref='group', lazy=True)


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    courses = db.relationship(
        'Course',
        secondary='student_courses',
        back_populates='students')


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    students = db.relationship(
        'Student',
        secondary='student_courses',
        back_populates='courses')

# As realtionship is many to many need an additional join table


class StudentCourses(db.Model):
    __tablename__ = 'student_courses'
    student_id = db.Column(
        db.Integer,
        db.ForeignKey('students.id'),
        primary_key=True)
    course_id = db.Column(
        db.Integer,
        db.ForeignKey('courses.id'),
        primary_key=True)
