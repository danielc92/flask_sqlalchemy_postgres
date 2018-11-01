import pandas
from datetime import datetime as dt
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, request, session, jsonify

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

    emp_id = db.Column(db.Integer, primary_key=True)
    emp_name = db.Column(db.String(255))
    emp_age = db.Column(db.Integer)

    def __repr__(self):
        return f'empid:{self.emp_id},emp_name:{self.emp_name},emp_age:{self.emp_age}'


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

        if emp_name and emp_age:
            
            user = Employee(emp_name=emp_name, emp_age=emp_age)
            db.session.add(user)
            db.session.commit()
            return jsonify({'Success':f'Inserted new record to database. {emp_name}, {emp_age}.'})
        else:
            
            return jsonify({'Error':'emp_name and emp_age parameters must be populated.'})

        

    except Exception as e:
        return jsonify({'Error':f'{e}'})


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
        emp = Employee.query.filter_by(emp_id=emp_id).one()
        db.session.delete(emp)
        db.session.commit()
        return jsonify({'Success':f'Removed employee with id {emp_id}'})

    except Exception as e:
        return jsonify({'Error':f'{e}'})


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

        data = pandas.read_sql(db.session.query(Employee).limit(limit).\
                               with_entities(Employee.emp_id, 
                                             Employee.emp_name, 
                                             Employee.emp_age)\
                               .statement, 
                               con=db.session.bind)

        format_ = request.args.get('format')

        if format_ == 'html':
            return data.to_html(index=False)
        else:
            response = data.to_json(orient='table')
            return jsonify({'Success':response,
                            'Timestamp': dt.now().strftime('%d-%m-%Y %H:%M:%S')})

    except Exception as e:
        response = jsonify({'Error':f'{e}'})
        return response


'''
This route queries the employee table and returns a query object string
Usage Example:
http://localhost:4999/show-employees-query
'''


@app.route('/show-employees-query')
def show_employee_q():
    try:

        query = Employee.query.all()
        return str(query)
    except Exception as e:

        return jsonify({'Error':f'{e}'})


'''
Execute app on port 4999 in debug mode
'''


if __name__ == "__main__":


    app.run(port=4999, debug=True)