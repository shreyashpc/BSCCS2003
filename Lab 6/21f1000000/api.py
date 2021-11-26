from flask import Flask, request, render_template, redirect, url_for, jsonify, abort, Response
from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, fields, marshal_with

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'
app.config['PROPAGATE_EXCEPTIONS'] = True

db = SQLAlchemy(app)


class APIException(Exception):
    def __init__(self, error_code, error_desc):
        self.error = dict(error_code=error_code, error_message=error_desc)


class Enrollment(db.Model):
    __tablename__ = "enrollment"

    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

    student = db.relationship('Student', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')


enrollment_fields = {
    'enrollment_id': fields.Integer,
    'student_id': fields.Integer,
    'course_id': fields.Integer
}


class Student(db.Model):
    __tablename__ = "student"

    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)


student_fields = {
    'student_id': fields.Integer,
    'roll_number': fields.String,
    'first_name': fields.String,
    'last_name': fields.String
}


class Course(db.Model):
    __tablename__ = "course"

    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)


course_fields = {
    'course_id': fields.Integer,
    'course_code': fields.String,
    'course_name': fields.String,
    'course_description': fields.String
}


def get_course(f):
    def f_wrapper(**kw):
        course_id = kw.pop('course_id')

        kw['course_obj'] = Course.query.get(course_id)
        if kw['course_obj'] is None:
            abort(404, 'Course not found')

        return f(**kw)

    return f_wrapper


def get_student(f):
    def f_wrapper(**kw):
        student_id = kw.pop('student_id')

        kw['student_obj'] = Student.query.get(student_id)
        if kw['student_obj'] is None:
            abort(404, 'Student not found')

        return f(**kw)

    return f_wrapper


def get_student_enrollment(f):
    def f_wrapper(**kw):
        student_id = kw.pop('student_id')

        kw['student_obj'] = Student.query.get(student_id)
        if kw['student_obj'] is None:
            return {'error_code': 'ENROLLMENT002', 'error_message': 'Student not found'}, 404

        return f(**kw)

    return f_wrapper


@api.resource('/api/course')
class CourseAPI(Resource):

    @marshal_with(course_fields)
    def post(self):
        data = request.json or request.form

        course_name = data.get('course_name')
        course_code = data.get('course_code')
        course_description = data.get('course_description')

        if not course_name or not isinstance(course_name, str):
            raise APIException("COURSE001", "Course Name is required and should be string.")

        elif not course_code or not isinstance(course_code, str):
            raise APIException("COURSE002", "Course Code is required and should be string.")

        elif course_description and not isinstance(course_description, str):
            raise APIException("COURSE003", "Course Description should be string.")

        course = Course.query.where(Course.course_code == course_code).first()
        if course is not None:
            abort(409, "course_code already exist")

        course = Course(course_name=course_name, course_code=course_code, course_description=course_description)
        db.session.add(course)
        db.session.commit()

        return course, 201


@api.resource('/api/course/<int:course_id>')
class CourseOperationsAPI(Resource):
    method_decorators = [get_course]

    @marshal_with(course_fields)
    def get(self, course_obj):
        return course_obj

    @marshal_with(course_fields)
    def put(self, course_obj):
        data = request.json or request.form

        course_name = data.get('course_name')
        course_code = data.get('course_code')
        course_description = data.get('course_description')

        if not course_name or not isinstance(course_name, str):
            raise APIException("COURSE001", "Course Name is required and should be string.")

        elif not course_code or not isinstance(course_code, str):
            raise APIException("COURSE002", "Course Code is required and should be string.")

        elif course_description and not isinstance(course_description, str):
            raise APIException("COURSE003", "Course Description should be string.")

        if course_obj.course_code != course_code:
            course = Course.query.where(Course.course_code == course_code).first()
            if course is not None:
                raise APIException("COURSE002", "Course Code already exists")

        course_obj.course_name = course_name
        course_obj.course_code = course_code
        course_obj.course_description = course_description if 'course_description' in data else course_obj.course_description

        db.session.add(course_obj)
        db.session.commit()

        return course_obj

    def delete(self, course_obj):
        enroll = course_obj.enrollments
        [db.session.delete(i) for i in enroll]

        db.session.delete(course_obj)
        db.session.commit()

        return Response(status=200)


@api.resource('/api/student')
class StudentAPI(Resource):

    def get(self):
        return {"lol": "mow"}

    @marshal_with(student_fields)
    def post(self):
        data = request.json or request.form

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        roll_number = data.get('roll_number')

        if not roll_number or not isinstance(roll_number, str):
            raise APIException("STUDENT001", "Roll Number required and should be String")

        elif not first_name or not isinstance(first_name, str):
            raise APIException("STUDENT002", "First Name is required and should be String")

        elif last_name and not isinstance(last_name, str):
            raise APIException("STUDENT003", "Last Name is String")

        student = Student.query.where(Student.roll_number == roll_number).first()
        if student is not None:
            abort(409, "Student already exist")

        student = Student(roll_number=roll_number, first_name=first_name, last_name=last_name)
        db.session.add(student)
        db.session.commit()

        return student, 201


@api.resource('/api/student/<int:student_id>')
class StudentOperationsAPI(Resource):
    method_decorators = [get_student]

    @marshal_with(student_fields)
    def get(self, student_obj):
        return student_obj

    @marshal_with(student_fields)
    def put(self, student_obj):
        data = request.json or request.form

        print(data, 'last_name' in data)

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        roll_number = data.get('roll_number')

        if not roll_number or not isinstance(roll_number, str):
            raise APIException("STUDENT001", "Roll Number required and should be String")

        elif not first_name or not isinstance(first_name, str):
            raise APIException("STUDENT002", "First Name is required and should be String")

        elif last_name and not isinstance(last_name, str):
            raise APIException("STUDENT003", "Last Name is String")

        if roll_number != student_obj.roll_number:
            student = Student.query.where(Student.roll_number == roll_number).first()
            if student is not None:
                raise APIException("STUDENT001", "Student already exists")

        student_obj.first_name = first_name
        student_obj.last_name = last_name if 'last_name' in data else student_obj.last_name
        student_obj.roll_number = roll_number

        db.session.add(student_obj)
        db.session.commit()

        return student_obj

    def delete(self, student_obj):
        enroll = student_obj.enrollments
        [db.session.delete(i) for i in enroll]

        db.session.delete(student_obj)
        db.session.commit()

        return Response(status=200)


@api.resource('/api/student/<int:student_id>/course')
class EnollmentAPI(Resource):
    method_decorators = [get_student_enrollment]

    @marshal_with(enrollment_fields)
    def get(self, student_obj):
        return student_obj.enrollments or abort(404, 'Student is not enrolled in any course')

    @marshal_with(enrollment_fields)
    def post(self, student_obj):
        data = request.json or request.form

        try:
            course_id = int(data.get('course_id'))
            assert course_id is not None
        except:
            raise APIException('ENROLLMENT003', 'Course ID is required and should be an integer')

        course = Course.query.get(course_id)
        if course is None:
            raise APIException('ENROLLMENT001', "Course does not exist")

        enrol = Enrollment.query.where(Enrollment.student_id == student_obj.student_id,
                                       Enrollment.course_id == course_id).first()
        if enrol is not None:
            abort(409, "Student already enrolled to the course")

        enrollment = Enrollment(student_id=student_obj.student_id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()

        return student_obj.enrollments, 201


@api.resource('/api/student/<int:student_id>/course/<int:course_id>')
class EnollmentOperationsAPI(Resource):

    def delete(self, student_id, course_id):
        e = Enrollment.query.where(Enrollment.student_id == student_id, Enrollment.course_id == course_id).first()
        if e is None:
            abort(404, "Enrollment for the student not found")

        db.session.delete(e)
        db.session.commit()

        return Response(status=200)


@app.errorhandler(APIException)
def handle_custom_exception(err):
    return jsonify(err.error), 400


@app.errorhandler(exc.SQLAlchemyError)
def handle_db_exceptions(error):
    db.session.rollback()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)