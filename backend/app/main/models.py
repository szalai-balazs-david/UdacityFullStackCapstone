from app.main import db


class Test(db.Model):
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    results = db.relationship('TestResult', cascade="delete", backref=db.backref('test', lazy=True))


class TestResult(db.Model):
    __tablename__ = 'test_results'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    auth0_id = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=True, unique=True)
    name = db.Column(db.String, nullable=True)
    results = db.relationship('TestResult', cascade="delete", backref='user', lazy=True)
