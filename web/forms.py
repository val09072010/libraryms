# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import Optional, DataRequired


class SearchForm(FlaskForm):
    search_title = StringField('Search by Book title')
    search_author = StringField('Search by Author')
    submit = SubmitField('Search')


class AddEditBookForm(FlaskForm):
    book_title = StringField("Book name", validators=[DataRequired()])
    book_genre = StringField("Genre", validators=[Optional()])
    authors = SelectField("Select author")
    submit = SubmitField("Add book")


class AddAuthorForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField("Last name", validators=[DataRequired()])
    submit = SubmitField("Add author")


class LoginForm(FlaskForm):
    login = StringField("Login or email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("SignUp")
