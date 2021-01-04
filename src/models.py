from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    skills = db.relationship('Skill', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "skills": list(map(lambda x: x.serialize(), self.skills))
            # do not serialize the password, its a security breach
        }

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_type = db.Column(db.String(120), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)

    def __repr__(self):
        return '<Skill %r>' % self.skill_type

    def serialize(self):
        return {
            "id": self.id,
            "skill_type": self.skill_type
            # do not serialize the password, its a security breach
        }

# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     addresses = db.relationship('Address', backref='person', lazy=True)

# class Address(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), nullable=False)
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
#         nullable=False)