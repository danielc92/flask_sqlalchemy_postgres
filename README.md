# Flask Postgres

A repository testing the interactions between postgres and flask using flask-sqlalchemy library and its ORM to map and pull data into flask.

# Setting up the database in postgres

```sql
Queries to set up database

CREATE TABLE employees
(
    emp_id SERIAL PRIMARY KEY,
    emp_name VARCHAR(255),
    emp_age INTEGER
)

CREATE TABLE complaints
(
    complaint_id SERIAL PRIMARY KEY,
    complaint_content VARCHAR(255),
    complaint_emp_id INTEGER REFERENCES employees (emp_id)
)
```

# Python Requirements
- pandas
- flask_sqlalchemy (documentation:http://flask-sqlalchemy.pocoo.org/2.3/queries/#querying-records)
- flask
- datetime

# Running app
`cd` into directory of project
`python main.py` or `python3 main.py`

# Futher details
Information about how to access routes are within the comments in `main.py`

