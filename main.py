'''
Documentation for sql-flaskalchemy: 
http://flask-sqlalchemy.pocoo.org/2.3/queries/#querying-records
'''

'''
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
'''


'''
Imports
'''
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
import pandas

'''
Initiate flask app 
'''
app = Flask(__name__)


'''
Initiate database
URI takes format <driver>://<username><password>@<server><port>/<database name>
'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/sqlalchemy'
db = SQLAlchemy(app)

'''
Create mapper object to table in postgres database
'''
class Employee(db.Model):

	__tablename__ = 'employees'
	
	emp_id = db.Column(db.Integer, primary_key = True)
	emp_name = db.Column(db.String(255))
	emp_age = db.Column(db.Integer)

	def __repr__(self):
		return 'empid:{},emp_name:{},emp_age:{}'\
		.format(self.emp_id, self.emp_name, self.emp_age)


'''
This route adds an new employee using url arguments.
Usage Example:
http://localhost:4999/add-employee?emp_name=daniel%20corcoran&emp_age=54
'''
@app.route('/add-employee')
def add_new_employee():
	try:
		emp_name = request.args.get('emp_name')
		emp_age = request.args.get('emp_age')
		user = Employee(emp_name = emp_name, emp_age = emp_age)
		db.session.add(user)
		db.session.commit()
		return 'Success'
	
	except Exception as e:
		return 'Failed to add employee. Error: {}'.format(e)


'''
This route will delete an employee using url argument.
Note: Won't work if emp id exists in foreign tables
Usage Example:
http://localhost:4999/remove-employee?emp_id=16
'''
@app.route('/remove-employee')
def remove_employee():
	try:
		emp_id = request.args.get('emp_id')
		emp = Employee.query.filter_by(emp_id = emp_id).one()
		db.session.delete(emp)
		db.session.commit()
		return 'Success'
	
	except Exception as e:
		return 'Failed to remove employee. Error: {}'.format(e)


'''
This route queries the employee table and returns a html table
?limit parameter can be used to return less rows 
Usage Example:
http://localhost:4999/show-employees-pandas
'''
@app.route('/show-employees-pandas')
def show_employee_p():
	try:
		limit = request.args.get('limit')

		if not limit:
			limit = 9999999999999

		print(limit)

		data = pandas.read_sql(db.session.query(Employee).limit(limit).\
			with_entities(Employee.emp_id, Employee.emp_name, Employee.emp_age)\
			.statement, con = db.session.bind)		

		return data.to_html(index = False)

	except Exception as e:

		return 'Failed to return data: error{}'.format(e)


'''
This route queries the employee table and returns a query object string
Usage Example:
http://localhost:4999/show-employees-query
'''
@app.route('/show-employees-query')
def show_employee_q():
	try:

		query = Employee.query.all()
		print(type(query))
		return str(query)
	except Exception as e:

		return 'Failed to return data: error{}'.format(e)


'''
Execute app on port 4999 in debug mode
'''
if __name__ == "__main__":
	app.run(port = 4999,
		debug = True)