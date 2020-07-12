from app.main import db


class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    users = db.relationship('User', backref='doctor', lazy=True)


class Test(db.Model):
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    results = db.relationship('TestResult', cascade="delete", backref=db.backref('venue', lazy=True))


class TestResult(db.Model):
    __tablename__ = 'test_results'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('Test.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('Doctor.id'), nullable=False)
    results = db.relationship('TestResult', backref='user', lazy=True)
