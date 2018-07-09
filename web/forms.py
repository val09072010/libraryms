# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectMultipleField, BooleanField
from wtforms.validators import Optional, DataRequired
from .resources import Resources as Res


class SearchForm(FlaskForm):
    search_title = StringField(Res.FORM_SEARCH_BY_TITLE)
    search_author = StringField(Res.FORM_SEARCH_BY_AUTHOR)
    submit = SubmitField(Res.SEARCH_ACTION)


class AddEditBookForm(FlaskForm):
    book_title = StringField(Res.FORM_ADD_EDIT_BOOK_TITLE, validators=[DataRequired()])
    book_genre = StringField(Res.FORM_ADD_EDIT_BOOK_GENRE, validators=[Optional()])
    authors = SelectMultipleField(Res.FORM_ADD_EDIT_BOOK_AUTHORS)
    submit = SubmitField(Res.FORM_ADD_EDIT_BOOK_SUBMIT)


class AddEditAuthorForm(FlaskForm):
    first_name = StringField(Res.FORM_ADD_AUTHOR_FNAME, validators=[DataRequired()])
    last_name = StringField(Res.FORM_ADD_AUTHOR_LNAME, validators=[DataRequired()])
    submit = SubmitField(Res.FORM_ADD_EDIT_AUTHOR_SUBMIT)


class LoginForm(FlaskForm):
    login = StringField(Res.FORM_LOGIN_LOGIN, validators=[DataRequired()])
    password = PasswordField(Res.FORM_LOGIN_PASS, validators=[DataRequired()])
    submit = SubmitField(Res.SIGNIN_ACTION)


class DeleteForm(FlaskForm):
    confirm_del = BooleanField(Res.FORM_DEL_CONFIRM, default=False, render_kw={'onclick': 'confirmDelete()'})
    submit = SubmitField(Res.DEL_BOOK_ACTION, id="confirmDeleteBtn", render_kw={'disabled': 'disabled'})
