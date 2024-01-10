from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import EmailType, PasswordType, ArrowType, DateTimeRangeType
import datetime

db = SQLAlchemy()


class Address(db.Model):
    IDAddress = db.Column(db.Integer, primary_key=True, nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    Longitude = db.Column(db.Integer, nullable=False)
    Latitude = db.Column(db.Integer, nullable=False)
    StreetName = db.Column(db.String(63))
    BuildingNumber = db.Column(db.Integer)
    FlatNumber = db.Column(db.Integer)
    CityName = db.Column(db.String(63))
    Province = db.Column(db.String(63))
    Country = db.Column(db.String(63))
    addressesUser = db.relationship('User', backref=db.backref('users', lazy=True))
    addressesEvent = db.relationship('Event', backref=db.backref('events', lazy=True))


class User(db.Model):
    IDUser = db.Column(db.Integer, primary_key=True, nullable=False)
    Email = db.Column(EmailType, nullable=False)
    Password = db.Column(PasswordType, nullable=False)
    Name = db.Column(db.String(63), nullable=False)
    Surname = db.Column(db.String(63), nullable=False)
    DateOfBirth = db.Column(ArrowType)
    IDAddress = db.Column(db.Integer, db.ForeignKey(Address.IDAddress))
    organisers = db.relationship('Event', backref=db.backref('events', lazy=True))
    participant = db.relationship('EventParticipant', backref=db.backref('participants', lazy=True))
    permission = db.relationship('Permission', backref=db.backref('permissions', lazy=True))


class Category(db.Model):
    IDCategory = db.Column(db.Integer, primary_key=True, nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    IDCategoryParent = db.Column(db.Integer)
    category = db.relationship('Event', backref=db.backref('events', lazy=True))


class Event(db.Model):
    IDEvent = db.Column(db.Integer, primary_key=True, nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    StartEndDateTime = db.Column(DateTimeRangeType)
    Capacity = db.Column(db.Integer)
    Price = db.Column(db.Integer)
    IDOrganiser = db.Column(db.Integer, db.ForeignKey(User.IDUser))
    IDAddress = db.Column(db.Integer, db.ForeignKey(Address.IDAddress))
    IDCategory = db.Column(db.Integer, db.ForeignKey(Category.IDCategory))
    participate = db.relationship('EventParticipant', backref=db.backref('participates', lazy=True))
    permission = db.relationship('Permission', backref=db.backref('permissions', lazy=True))


class EventParticipant(db.Model):
    IDUser = db.Column(db.Integer, db.ForeignKey(User.IDUser), primary_key=True, nullable=False)
    IDEvent = db.Column(db.Integer, db.ForeignKey(Event.IDEvent), primary_key=True, nullable=False)
    Review = db.Column(db.Integer)


class Role:
    IDRole = db.Column(db.Integer, primary_key=True, nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    LastUpdate = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    CreatDate = db.Column(db.DateTime, default=datetime.datetime.now)
    permission = db.relationship('Permission', backref=db.backref('permissions', lazy=True))


class Permission:
    IDPermission = db.Column(db.Integer, primary_key=True, nullable=False)
    IDUser = db.Column(db.Integer, db.ForeignKey(User.IDUser), nullable=False)
    IDRole = db.Column(db.Integer, db.ForeignKey(Role.IDRole), nullable=False)
    IDEvent = db.Column(db.Integer, db.ForeignKey(Event.IDEvent), nullable=False)
    LastUpdate = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    CreatDate = db.Column(db.DateTime, default=datetime.datetime.now)
