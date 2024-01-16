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
    addressUser = db.relationship('User', back_populates='userAddress', lazy=True)
    addressEvent = db.relationship('Event', back_populates='eventAddress', lazy=True)

    def __repr__(self):
        return f"Address: ID: {self.IDAddress}, Name: {self.Name}, Longitude: {self.Longitude}, " \
               f"Latitude: {self.Latitude}, Street Name: {self.StreetName}, Building Number: {self.BuildingNumber}" \
               f"Flat Number {self.FlatNumber}, CityName: {self.CityName}, Province: {self.Province}, " \
               f"Country: {self.Country}"


class User(db.Model):
    IDUser = db.Column(db.Integer, primary_key=True, nullable=False)
    Email = db.Column(EmailType, nullable=False, unique=True)
    Password = db.Column(PasswordType, nullable=False)
    Name = db.Column(db.String(63), nullable=False)
    Surname = db.Column(db.String(63), nullable=False)
    DateOfBirth = db.Column(ArrowType)
    IDAddress = db.Column(db.Integer, db.ForeignKey(Address.IDAddress))
    userAddress = db.relationship('Address', back_populates='addressUser', lazy=True)
    userEventParticipant = db.relationship('EventParticipant', back_populates='eventParticipantUser', lazy=True)
    userPermission = db.relationship('Permission', back_populates='permissionUser', lazy=True)
    userEvent = db.relationship('Event', back_populates='eventUser', lazy=True)

    def __repr__(self):
        return f"User IDUser: {self.IDUser}, Email: {self.Email}, Password: {self.Password}, Name: {self.Name}, " \
               f"Surname: {self.Surname} Date of birth: {self.DateOfBirth}, IDAddress: {self.IDAddress}"


class Category(db.Model):
    IDCategory = db.Column(db.Integer, primary_key=True, nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    IDCategoryParent = db.Column(db.Integer)
    categoryEvent = db.relationship('Event',  back_populates='eventCategory', lazy=True)

    def __repr__(self):
        return f"Category IDCategory: {self.IDCategory}, Name: {self.Name}, IDCategoryParent: {self.IDCategoryParent}"


class Event(db.Model):
    IDEvent = db.Column(db.Integer, primary_key=True, nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    StartEndDateTime = db.Column(DateTimeRangeType)
    Capacity = db.Column(db.Integer)
    Price = db.Column(db.Integer)
    IDOrganiser = db.Column(db.Integer, db.ForeignKey(User.IDUser))
    eventUser = db.relationship('User', back_populates='userEvent', lazy=True)
    IDAddress = db.Column(db.Integer, db.ForeignKey(Address.IDAddress))
    eventAddress = db.relationship('Address', back_populates='addressEvent', lazy=True)
    IDCategory = db.Column(db.Integer, db.ForeignKey(Category.IDCategory))
    eventCategory = db.relationship('Category',  back_populates='categoryEvent', lazy=True)
    eventParticipantEventFrom = db.relationship('EventParticipant', back_populates='eventParticipantEventTo', lazy=True)
    permissionEvent = db.relationship('Permission', back_populates='eventPermission', lazy=True)

    def __repr__(self):
        return f"Event ID: {self.IDEvent}, Name: {self.Name}, StartEndDate: {self.StartEndDateTime}," \
               f" Capacity: {self.Capacity}, Price: {self.Price}, IDCategory: {self.IDCategory}"


class EventParticipant(db.Model):
    IDUser = db.Column(db.Integer, db.ForeignKey(User.IDUser), primary_key=True, nullable=False)
    eventParticipantUser = db.relationship('User', back_populates='userEventParticipant', lazy=True)
    IDEvent = db.Column(db.Integer, db.ForeignKey(Event.IDEvent), primary_key=True, nullable=False)
    eventParticipantEventTo = db.relationship('Event', back_populates='eventParticipantEventFrom', lazy=True)
    Review = db.Column(db.Integer)

    def __repr__(self):
        return f"IDUser {self.IDUser}, IDEvent {self.IDEvent}, Review {self.Review}"


class Role(db.Model):
    IDRole = db.Column(db.Integer, primary_key=True, nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    LastUpdate = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    CreatDate = db.Column(db.DateTime, default=datetime.datetime.now)
    rolePermission = db.relationship('Permission', back_populates='permissionRole', lazy=True)

    def __repr__(self):
        return f"Role IDRole: {self.IDRole}, Name: {self.Name}, LastUpdate: {self.LastUpdate}," \
               f" CreateDate: {self.CreatDate}"


class Permission(db.Model):
    IDPermission = db.Column(db.Integer, primary_key=True, nullable=False)
    IDUser = db.Column(db.Integer, db.ForeignKey(User.IDUser), nullable=False)
    permissionUser = db.relationship('User', back_populates='userPermission', lazy=True)
    IDRole = db.Column(db.Integer, db.ForeignKey(Role.IDRole), nullable=False)
    permissionRole = db.relationship('Role', back_populates='rolePermission', lazy=True)
    IDEvent = db.Column(db.Integer, db.ForeignKey(Event.IDEvent), nullable=False)
    eventPermission = db.relationship('Event', back_populates='permissionEvent', lazy=True)
    LastUpdate = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    CreatDate = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"IDPermission: {self.IDPermission}, IDUser: {self.IDUser}, IDRole {self.IDRole}," \
               f" IDEvent: {self.IDEvent} LastUpdate: {self.LastUpdate}, CreateDate: {self.CreatDate}"
