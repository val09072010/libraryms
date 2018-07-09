# -*- coding: utf-8 -*-
from web import web, db, core
from werkzeug.urls import url_parse
from flask import render_template, redirect, url_for, session, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from .forms import SearchForm, AddEditBookForm, AddAuthorForm, LoginForm, DeleteForm
from .models import Author, User
from .resources import Resources as Res


@web.route('/')
@web.route('/index')
def index():
    return render_template("index.html", title=Res.TITLE)


@web.route('/results')
def results():
    current_books = []
    book_not_found_msg = Res.NOTHING_FOUND
    if 'books' in session:
        current_books = session['books']
    return render_template("results.html", books=current_books, title=Res.TITLE, page_action=Res.RESULT_ACTION,
                           msg=book_not_found_msg)


@web.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        title_to_search = form.search_title.data.strip()
        author_to_search = form.search_author.data.strip()
        search_text = ""
        if title_to_search:
            criteria = core.SEARCH_BY_TITLE
            search_text = title_to_search
        elif author_to_search:
            criteria = core.SEARCH_BY_AUTHOR_LASTNAME
            search_text = author_to_search
        else:
            criteria = core.SEARCH_ALL
        session['books'] = core.search_book(search_text, criteria=criteria, serialize=True)
        return redirect(url_for("results"))
    return render_template("search.html", form=form, title=Res.TITLE, page_action=Res.SEARCH_ACTION)


@web.route('/edit_book/<book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    form = prepare_add_edit_book_form()
    if form.validate_on_submit():
        title = form.book_title.data.strip()
        genre = form.book_genre.data.strip()
        author_ids = form.authors.data
        book = core.update_book(book_id, title, genre, author_ids)
        flash(Res.FLASH_EDIT_BOOK.format(book.title, book.genre, book.authors))
        return redirect(url_for('index'))
    elif request.method == 'GET':
        book = core.get_book_by_id(book_id)
        form.authors.default = str(book.authors[0].id)
        form.process()
        form.book_title.data = book.title
        form.book_genre.data = book.genre
    return render_template("add_edit_book.html", form=form, title=Res.TITLE, page_action=Res.EDIT_BOOK_ACTION)


@web.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = prepare_add_edit_book_form()
    if form.validate_on_submit():
        title = form.book_title.data.strip()
        genre = form.book_genre.data.strip()
        author_ids = form.authors.data
        book = core.store_book(title, genre, author_ids)
        flash(Res.FLASH_ADD_BOOK.format(book.title, book.genre, book.authors))
        return redirect(url_for('index'))
    return render_template("add_edit_book.html", form=form, title=Res.TITLE, page_action=Res.ADD_BOOK_ACTION)


def prepare_add_edit_book_form():
    form = AddEditBookForm()
    form.authors.choices = list((str(i.id), i) for i in db.session.query(Author).all())
    return form


@web.route('/add_author', methods=['GET', 'POST'])
@login_required
def add_author():
    form = AddAuthorForm()
    if form.validate_on_submit():
        last_name = form.last_name.data.strip()
        existing_authors = db.session.query(Author).filter_by(last_name=last_name).all()
        if existing_authors and len(existing_authors) > 0:
            form.errors['author'] = Res.ADD_AUTHOR_ERROR
        else:
            author = Author(form.first_name.data.strip(), last_name)
            db.session.add(author)
            db.session.commit()
            flash(Res.FLASH_ADD_AUTHOR.format(author.id, author.first_name, author.last_name))
            return redirect(url_for('index'))
    return render_template("add_author.html", form=form, title=Res.TITLE, page_action=Res.ADD_AUTHOR_ACTION)


@web.route('/delete_book/<book_id>', methods=['POST', 'GET'])
@login_required
def del_book(book_id):
    form = DeleteForm()
    if form.validate_on_submit():
        deleted_book_title, deleted_book_genre = core.delete_book(book_id)
        flash(Res.FLASH_DEL_BOOK.format(deleted_book_title, deleted_book_genre))
        return redirect(url_for('index'))
    else:
        deleted_book = core.get_book_by_id(book_id)
        return render_template("delete.html", form=form, ask_for_confirmation=Res.FORM_DEL_ASK,
                               title=Res.TITLE, page_action=Res.DEL_BOOK_ACTION, book=deleted_book)


@web.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(login=form.login.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(Res.LOGIN_ERROR)
            return redirect(url_for('login'))
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", form=form, title=Res.TITLE, page_action=Res.SIGNIN_ACTION)


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
