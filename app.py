from flask import Flask, request, flash, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)

ma = Marshmallow(app)

class student(db.Model):
   id = db.Column('students.id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   city = db.Column(db.String(50))
   addr = db.Column(db.String(200)) 
   pin = db.Column(db.String(10))

   def __init__(self, name, city, addr,pin):
      self.name = name
      self.city = city
      self.addr = addr
      self.pin = pin

class studentSchema(ma.Schema):
   class Meta:
      fields = ('id', 'name', 'city', 'addr', 'pin')

student_schema = studentSchema()
students_schema = studentSchema(many=True)



@app.route('/', methods = ['GET', 'POST'])
def show_all():

   if request.method == 'POST':

      name = request.json['name']
      city = request.json['city']
      addr = request.json['addr']
      pin = request.json['pin']
      new_student = student(name, city, addr, pin)
      db.session.add(new_student)
      db.session.commit()
      return student_schema.jsonify(new_student)


   if request.method == 'GET':
      all_students = student.query.all()
      result = students_schema.dump(all_students).data
      return jsonify(result)


@app.route('/operation/<id>', methods = ['GET', 'PUT', 'DELETE'])
def operation(id):

   if request.method == 'GET':
      stu = student.query.get(id)
      return student_schema.jsonify(stu)

   if request.method == 'PUT':
      stu = student.query.get(id)
      name = request.json['name']
      city = request.json['city']
      addr = request.json['addr']
      pin = request.json['pin']
      stu.name=name
      stu.city=city
      stu.addr=addr
      stu.pin=pin
      db.session.commit()
      return student_schema.jsonify(stu)

   if request.method == 'DELETE':

      std = student.query.get(id)
      db.session.delete(std)
      db.session.commit()
      return student_schema.jsonify(std)

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)