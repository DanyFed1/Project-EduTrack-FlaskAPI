import pytest
from unittest.mock import patch
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    #'postgresql://master_user:test_password_for_master_user@localhost/fxmnd_task_10'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()  # Create tables for all models
        yield app.test_client()  # This client will have application context
        db.session.remove()
        db.drop_all()

class MockModel:
    """Simple class that mimics SQLAlchemy model to avoid a a discrepancy between
    the mocked return values and API resource methods expecting to interact class attributes."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

# Mock the queries.py functions
@patch('api_resources.find_all_groups')
def test_get_all_groups(mock_find_all_groups, client):
    mock_find_all_groups.return_value = [MockModel(id=1, name='Group A')]
    response = client.get('/groups')
    assert response.status_code == 200
    assert b'Group A' in response.data

@patch('api_resources.find_student_by_id')
def test_get_student_by_id(mock_find_student_by_id, client):
    mock_find_student_by_id.return_value = MockModel(id=1, first_name='John', last_name='Doe')
    response = client.get('/students/1')
    assert response.status_code == 200
    assert b'John' in response.data

@patch('api_resources.add_new_student')
def test_add_new_student(mock_add_new_student, client):
    mock_add_new_student.return_value = {'message': 'Student added successfully', 'student_id': 1}
    response = client.post('/students', json={'first_name': 'Jane', 'last_name': 'Doe', 'group_id': 1})
    assert response.status_code == 200
    assert b'Student added successfully' in response.data

@patch('api_resources.delete_student_by_id')
def test_delete_student_by_id(mock_delete_student_by_id, client):
    mock_delete_student_by_id.return_value = {'message': 'Student deleted successfully'}
    response = client.delete('/students/1')
    assert response.status_code == 200
    assert b'Student deleted successfully' in response.data

@patch('api_resources.find_students_by_course_id')
def test_get_students_by_course_id(mock_find_students_by_course_id, client):
    mock_find_students_by_course_id.return_value = [MockModel(id=1, first_name='John', last_name='Doe')]
    response = client.get('/courses/students/1')
    assert response.status_code == 200
    assert b'John' in response.data
@patch('api_resources.find_course_by_id')
def test_get_course_by_id(mock_find_course_by_id, client):
    mock_find_course_by_id.return_value = MockModel(id=1, name='Math', description='Algebra and Geometry')
    response = client.get('/courses/1')
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Math' in content and 'Algebra and Geometry' in content

@patch('api_resources.find_all_courses')
def test_get_all_courses(mock_find_all_courses, client):
    mock_find_all_courses.return_value = [
        MockModel(id=1, name='Math', description='Algebra and Geometry'),
        MockModel(id=2, name='Science', description='Physics and Chemistry')
    ]
    response = client.get('/courses')
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Math' in content and 'Science' in content

@patch('api_resources.add_student_to_courses')
def test_add_student_to_courses(mock_add_student_to_courses, client):
    mock_add_student_to_courses.return_value = None  # Assuming void function
    response = client.post('/students/1/courses', json={'course_id': [1, 2]})
    assert response.status_code == 200
    assert b'Students assigned to course successfully' in response.data

@patch('api_resources.remove_student_from_course')
def test_remove_student_from_course(mock_remove_student_from_course, client):
    mock_remove_student_from_course.return_value = None  # Assuming void function
    response = client.delete('/students/1/courses/1')
    assert response.status_code == 200
    assert b'Student removed from course successfully' in response.data