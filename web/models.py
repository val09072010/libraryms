# -*- coding: utf-8 -*-
from web import db, lm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

_TABLE_BOOKS = "books"
_TABLE_AUTHORS = "authors"
_TABLE_REL = "books_authors"
_TABLE_USERS = "users"
ROLE_ADMIN = 1
ROLE_USER = 0


class Book(db.Model):
    __tablename__ = _TABLE_BOOKS

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    genre = db.Column(db.String)

    authors = db.relationship('Author', secondary='books_authors', back_populates='books')

    def __init__(self, title, genre, authors):
        self.title = title
        self.genre = genre
        self.authors = authors

    def __repr__(self):
        return "Book #{0}: {1} ({2}) - {3}.".format(self.id, self.title, self.genre, self.authors)

    @property
    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'genre': self.genre, 'authors': self.serialize_authors}

    @property
    def serialize_authors(self):
        authors_list = map(str, self.authors)
        return ','.join(authors_list)


class Author(db.Model):
    __tablename__ = _TABLE_AUTHORS

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    books = db.relationship('Book', secondary='books_authors', back_populates='authors')

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    @property
    def to_dict(self):
        return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name}


class BooksAuthors(db.Model):
    __tablename__ = _TABLE_REL
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id', ondelete='CASCADE'), primary_key=True)


class User(UserMixin, db.Model):
    __tablename__ = _TABLE_USERS

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __init__(self, email, password, role):
        self.login = email
        self.set_password(password)
        self.role = role

    def set_password(self, pass_phrase):
        self.password_hash = generate_password_hash(pass_phrase)

    def check_password(self, pass_phrase):
        return check_password_hash(self.password_hash, pass_phrase)

    def __repr__(self):
        return "User {0}: {1}".format(self.id, self.login)


@lm.user_loader
def load_user(usr_id):
    return User.query.get(int(usr_id))
