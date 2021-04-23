from datetime import datetime

from flask_project import db


user_part = db.Table('users_patriarchs',
                     db.Column('userId', db.Integer, db.ForeignKey('users.useId')),
                     db.Column('partId', db.Integer, db.ForeignKey('patriarchs.partId')),
                     comment='realize the many-to-many between users and patriarchs')

part_stu = db.Table('patriarchs_students',
                    db.Column('partId', db.Integer, db.ForeignKey('patriarchs.partId')),
                    db.Column('stuId', db.Integer, db.ForeignKey('students.stuId')),
                    comment='realize the many-to-many between students and patriarchs')

user_teacher = db.Table('users_teachers',
                        db.Column('useId', db.Integer, db.ForeignKey('users.useId')),
                        db.Column('teaId', db.Integer, db.ForeignKey('teachers.teaId')),
                        comment='realize the many-to-many between users and teacher')

tea_cla = db.Table('teachers_classes',
                   db.Column('teaId', db.Integer, db.ForeignKey('teachers.teaId')),
                   db.Column('claId', db.Integer, db.ForeignKey('classes.claId')),
                   comment='realize the many-to-many between teachers and classes')

tea_sub = db.Table('teachers_subjects',
                   db.Column('teaId', db.Integer, db.ForeignKey('teachers.teaId')),
                   db.Column('subId', db.Integer, db.ForeignKey('subjects.subId')),
                   comment='realize the many-to-many between teachers and subjects')


cla_stu = db.Table('classes_students',
                   db.Column('claId', db.Integer, db.ForeignKey('classes.claId')),
                   db.Column('stuId', db.Integer, db.ForeignKey('students.stuId')),
                   comment='realize the many-to-many between grades and students')

sub_stu = db.Table('subjects_students',
                   db.Column('subId', db.Integer, db.ForeignKey('subjects.subId')),
                   db.Column('stuId', db.Integer, db.ForeignKey('students.stuId')),
                   comment='realize the many-to-many between subjects and students')


class BaseModel(db.Model):
    """
    Implementation of the basic method and basic fields
    """
    __abstract__ = True

    status = db.Column(db.SmallInteger, comment='status')
    timeCreate = db.Column(db.DateTime, default=datetime.now, comment=' created time')
    timeModified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='updated time')


class Users(BaseModel):
    """
    users are used as basic information tables
    """

    __tablename__ = 'users'

    useId = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='foreign key')
    openId = db.Column(db.String(128), nullable=False, unique=True, comment='openid')
    username = db.Column(db.String(64), index=True, unique=True, comment='actual name')
    nickname = db.Column(db.String(64), comment='nick name')
    mobile = db.Column(db.String(11), index=True, unique=True, comment='mobile')
    email = db.Column(db.String(128), index=True, unique=True, comment='email')
    sex = db.Column(db.SmallInteger, comment='sex')
    age = db.Column(db.String(128), comment='age')
    avatar = db.Column(db.String(128), nullable=False)
    isDelete = db.Column(db.Boolean, default=False, comment='whether to logical deletion')
    isActive = db.Column(db.Boolean, default=False, comment='whether to active')
    isBase = db.Column(db.Boolean, default=False)
    isShow = db.Column(db.Boolean, default=False, comment='whether to show user information ')
    identifyId = db.Column(db.SmallInteger, comment='whether to judge the user identify')
    part = db.relationship('Patriarchs',
                           secondary=user_part,
                           backref=db.backref('users', lazy='dynamic'),
                           lazy='dynamic')
    teacher = db.relationship('Teachers',
                              secondary=user_teacher,
                              backref=db.backref('users', lazy='dynamic'),
                              lazy='dynamic')

    @classmethod
    def get(cls, openid):
        return cls.query.filter_by(openId=openid).first()

    @classmethod
    def add(cls, openid):
        if openid is not None:
            user = cls
            user.openId = openid
            db.session.add(user)
            db.session.commit()
            return user


class Patriarchs(BaseModel):
    """
    patriarchs
    """

    __tablename__ = 'patriarchs'

    partId = db.Column(db.Integer, index=True, primary_key=True, comment='foreign key')
    username = db.Column(db.String(128), unique=True, comment='actual name')
    mobile = db.Column(db.String(11), comment='mobile')
    sex = db.Column(db.SmallInteger, comment='sex')
    age = db.Column(db.String(128), comment='age ')
    isHasClass = db.Column(db.Boolean, default=False, comment='whether to add class')
    student = db.relationship('Students',
                              secondary=part_stu,
                              backref=db.backref('students', lazy='dynamic'),
                              lazy='dynamic')


class Schools(BaseModel):

    """
    schools
    """

    __tablename__ = 'schools'

    schId = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='foreign key')
    schoolName = db.Column(db.String(128), comment='school name')
    schoolCode = db.Column(db.String(255), index=True, unique=True, comment='school identification code')
    educationTypeName = db.Column(db.String(128), comment='school system name')
    periodName = db.Column(db.String(128), comment='school section')
    telephone = db.Column(db.String(11), comment='school telephone')
    grades = db.relationship('Grades', backref="grades", cascade='all')


class Teachers(BaseModel):
    """
    teachers
    """

    __tablename__ = 'teachers'

    teaId = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='foreign key')
    username = db.Column(db.String(128), index=True, unique=True, comment='actual name')
    nickname = db.Column(db.String(64), comment='nick name')
    sex = db.Column(db.SmallInteger, comment='sex')
    email = db.Column(db.String(128), index=True, unique=True, comment='email')
    mobile = db.Column(db.String(11), index=True, unique=True, comment='mobile')
    age = db.Column(db.String(128))
    isDeleted = db.Column(db.Boolean, default=False, comment='logical deletion')
    isActive = db.Column(db.Boolean, default=False, comment='whether to active')
    isBase = db.Column(db.Boolean, default=False, comment='whether to activate basic services ')
    isShow = db.Column(db.Boolean, default=False, comment='whether to show teacher information')
    isHeadTeacher = db.Column(db.Boolean, default=False, comment='whether to judge headteacher')
    isHasClass = db.Column(db.Boolean, default=False, comment='whether to add class')
    cla = db.relationship('classes',
                          secondary=tea_cla,
                          backref=db.backref('classes', lazy='dynamic'),
                          lazy='dynamic')

    subject = db.relationship('subjects',
                              secondary=tea_sub,
                              backref=db.backref('subjects', lazy='dynamic'),
                              lazy='dynamic')


class Grades(BaseModel):
    """
    grades
    """

    __tablename__ = 'grades'

    graId = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='foreign key')
    gradeCode = db.Column(db.Integer, index=True, unique=True, comment='grade code')
    gradeName = db.Column(db.String(128), unique=True, comment='grade name')
    isGraduate = db.Column(db.Boolean, default=False, comment='whether graduate')
    schId = db.Column(db.Integer, db.ForeignKey('schools.schId'), comment='achieve one-to-many')
    classes = db.relationship('Classes', backref="classes", cascade='all')


class Classes(BaseModel):
    """
    class
    """
    __tablename__ = 'classes'

    claId = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='foreign key')
    className = db.Column(db.String(128), unique=True, comment='class name')
    class_types = db.Column(db.SmallInteger, comment='class types')
    graId = db.Column(db.Integer, db.ForeignKey('grades.graId'), comment='achieve one-to-many')
    student = db.relationship('students',
                              secondary=cla_stu,
                              backref=db.backref('classes', lazy='dynamic'),
                              lazy='dynamic')


class Subjects(BaseModel):
    """
    subjects
    """

    __tablename__ = 'subjects'

    subId = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='foreign key')
    subjectId = db.Column(db.String(255), index=True, unique=True, comment='subject code')
    subjectName = db.Column(db.String(128), comment='subject name')
    student = db.relationship('students',
                              secondary=sub_stu,
                              backref=db.backref('students', lazy='dynamic'),
                              lazy='dynamic')


class Students(BaseModel):
    """
    students
    """

    __tablename__ = 'students'

    stuId = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='foreign key')
    username = db.Column(db.String(128), index=True, unique=True, comment='actual name')
    nickname = db.Column(db.String(64), comment='nick name')
    sex = db.Column(db.SmallInteger, comment='sex')
    email = db.Column(db.String(128), index=True, unique=True, comment='email')
    mobile = db.Column(db.String(11), index=True, unique=True, comment='mobile')
    age = db.Column(db.String(128), comment='')
    isDeleted = db.Column(db.Boolean, default=False, comment='whether logical deletion')
    isActive = db.Column(db.Boolean, default=False, comment='whether to active')
    isBase = db.Column(db.Boolean, default=False, comment='whether to activate basic services')
    isShow = db.Column(db.Boolean, default=False, comment='whether to show student information')
    isHasClass = db.Column(db.Boolean, default=True, comment='whether to add class')
    relatives = db.Column(db.SmallInteger, comment='kinship')










