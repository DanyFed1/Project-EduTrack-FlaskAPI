# EduTrack

EduTrack is a Flask and SQLAlchemy-based RESTful API designed to manage educational data, specifically groups, students, and courses within an educational institution. Utilizing a PostgreSQL database, it enables CRUD operations (Create, Read, Update, Delete) on these entities, alongside providing relationships between students and courses to reflect real-world educational scenarios.

## Project Overview

The project was built to fulfill a comprehensive set of requirements, encompassing database setup, application development, and test-driven development. Key features include:

- **Database Initialization**: Scripts to create a PostgreSQL database, users, and tables with appropriate privileges and structures.
- **Data Generation**: Automated creation of test data, including groups, courses, and students with many-to-many relationships between students and courses.
- **ORM Queries**: Implementation of Object-Relational Mapping (ORM) queries to interact with the database, providing functionalities like adding students, finding groups with a certain number of students, and more.
- **RESTful API**: Development of a RESTful API using Flask and Flask-RESTful to manage educational data, with endpoints for groups, students, and courses.
- **Documentation and Testing**: Comprehensive testing of the API functionalities using pytest and documentation of API endpoints using Swagger.


### Initialize the database:
Execute the SQL scripts found in db_init_usr_gen.sql and table_creation.sql on your PostgreSQL server to set up the database, users, tables, and privileges.

Populate the database with initial data:
Run populate_empty_db.py to fill the database with initial test data.

